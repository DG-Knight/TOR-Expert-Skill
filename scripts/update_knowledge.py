"""อัปเดตคลังความรู้จาก Manifest แบบ staging-first

โหลดเฉพาะ URL HTTPS ของหน่วยงานรัฐ ตรวจ PDF ก่อนแทนไฟล์ จริง และสร้างรายงานที่ตรวจย้อนได้"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

try:
    from scripts.validate_knowledge import inspect_pdf
except ModuleNotFoundError:  # รองรับการเรียกไฟล์โดยตรงจาก scripts/
    from validate_knowledge import inspect_pdf


MAX_DOWNLOAD_BYTES = 100 * 1024 * 1024
OFFICIAL_HOSTS = {"ratchakitcha.soc.go.th", "www.ratchakitcha.soc.go.th"}


def validate_source_url(url: str) -> tuple[bool, str]:
    parsed = urllib.parse.urlparse(url.strip())
    host = (parsed.hostname or "").lower()
    if parsed.scheme.lower() != "https":
        return False, "source URL ต้องเป็น HTTPS"
    if host not in OFFICIAL_HOSTS and not host.endswith(".go.th"):
        return False, "source URL ไม่ใช่โดเมนราชการที่อนุญาต"
    return True, ""


def validate_staged_pdf(path: Path) -> dict[str, object]:
    return inspect_pdf(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_install(
    staged: Path,
    target: Path,
    validator: Callable[[Path], bool],
    archive_dir: Path | None = None,
) -> Path | None:
    if not validator(staged):
        raise ValueError(f"ไฟล์ staging ไม่ผ่านการตรวจ: {staged}")
    target.parent.mkdir(parents=True, exist_ok=True)
    archived: Path | None = None
    if target.exists() and archive_dir is not None:
        archive_dir.mkdir(parents=True, exist_ok=True)
        archived = archive_dir / target.name
        if archived.exists():
            archived = archive_dir / f"{target.stem}-{sha256_file(target)[:12]}{target.suffix}"
        shutil.copy2(target, archived)
    os.replace(staged, target)
    return archived


def build_report(records: list[dict[str, object]]) -> dict[str, object]:
    summary = Counter(str(record["action"]) for record in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": dict(sorted(summary.items())),
        "records": records,
    }


def _download(url: str, destination: Path, timeout: int) -> None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "TOR-Expert-Knowledge-Updater/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        destination.parent.mkdir(parents=True, exist_ok=True)
        total = 0
        with destination.open("wb") as stream:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_DOWNLOAD_BYTES:
                    raise ValueError("ไฟล์ดาวน์โหลดใหญ่เกิน 100 MB")
                stream.write(chunk)


def _safe_target(root: Path, local_path: str) -> Path:
    target = (root / local_path).resolve()
    if root.resolve() not in target.parents:
        raise ValueError("local_path อยู่นอกโฟลเดอร์โปรเจกต์")
    return target


def update_manifest(
    manifest_path: Path,
    root: Path,
    report_path: Path,
    *,
    apply: bool = False,
    timeout: int = 30,
) -> dict[str, object]:
    staging = Path(tempfile.mkdtemp(prefix="tor-knowledge-", dir=root / "tmp"))
    records: list[dict[str, object]] = []
    try:
        with manifest_path.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        for row in rows:
            item_id = row["id"]
            url = row.get("direct_file_url", "").strip()
            local_path = row.get("local_path", "").strip()
            if not url or not local_path:
                records.append(
                    {"id": item_id, "action": "blocked", "reason": "ไม่มี URL หรือ local_path"}
                )
                continue
            allowed, reason = validate_source_url(url)
            if not allowed:
                records.append({"id": item_id, "action": "blocked", "reason": reason})
                continue
            try:
                target = _safe_target(root, local_path)
                staged = staging / f"{item_id}.pdf"
                _download(url, staged, timeout)
                pdf_report = validate_staged_pdf(staged)
                if not pdf_report["valid"]:
                    raise ValueError("; ".join(pdf_report["errors"]))
                remote_hash = sha256_file(staged)
                current_hash = sha256_file(target) if target.exists() else ""
                if remote_hash == current_hash:
                    records.append(
                        {"id": item_id, "action": "unchanged", "sha256": remote_hash}
                    )
                elif apply:
                    archived = atomic_install(
                        staged,
                        target,
                        lambda path: bool(validate_staged_pdf(path)["valid"]),
                        root / "TOR_EXPERT_CURRENT_KNOWLEDGE" / "99_SUPERSEDED_ARCHIVE" / "updates",
                    )
                    record = {"id": item_id, "action": "installed", "sha256": remote_hash}
                    if archived:
                        record["archived_previous"] = str(archived.relative_to(root))
                    records.append(record)
                else:
                    records.append(
                        {"id": item_id, "action": "available_update", "sha256": remote_hash}
                    )
            except (OSError, ValueError, urllib.error.URLError) as exc:
                records.append({"id": item_id, "action": "error", "reason": str(exc)})
    finally:
        for path in staging.glob("*"):
            path.unlink(missing_ok=True)
        staging.rmdir()
    report = build_report(records)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="ตรวจและอัปเดตคลังความรู้จาก Manifest")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="ติดตั้งไฟล์ที่ตรวจผ่านแล้ว")
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    report = update_manifest(
        args.manifest,
        args.root,
        args.report,
        apply=args.apply,
        timeout=args.timeout,
    )
    print(json.dumps(report["summary"], ensure_ascii=False, sort_keys=True))
    return 0 if report["summary"].get("error", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
