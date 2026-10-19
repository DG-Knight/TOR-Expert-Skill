"""ตรวจความสมบูรณ์ของไฟล์และทะเบียนคลังความรู้ TOR Expert"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from pypdf import PdfReader


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_pdf(path: Path) -> dict[str, object]:
    errors: list[str] = []
    if not path.exists():
        return {"valid": False, "pages": 0, "errors": ["ไม่พบไฟล์"]}
    if path.read_bytes()[:5] != b"%PDF-":
        errors.append("ลายเซ็นไฟล์")
        return {"valid": False, "pages": 0, "errors": errors}
    try:
        pages = len(PdfReader(path).pages)
    except Exception as exc:  # pypdf ให้รายละเอียดข้อผิดพลาดตามไฟล์จริง
        errors.append(f"เปิด PDF ไม่ได้: {exc}")
        pages = 0
    if pages < 1:
        errors.append("ไม่มีหน้าเอกสาร")
    return {"valid": not errors, "pages": pages, "errors": errors}


def validate_manifest_files(manifest_path: Path, root: Path) -> dict[str, object]:
    errors: list[str] = []
    checked = 0
    with manifest_path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        local_path = row.get("local_path", "").strip()
        if not local_path:
            continue
        checked += 1
        path = root / local_path
        if not path.exists():
            errors.append(f"{row['id']}: ไม่พบไฟล์ {local_path}")
            continue
        expected_hash = row.get("sha256", "").strip().lower()
        if expected_hash and sha256_file(path) != expected_hash:
            errors.append(f"{row['id']}: ค่า SHA-256 ไม่ตรง")
        if path.suffix.lower() == ".pdf":
            report = inspect_pdf(path)
            if not report["valid"]:
                errors.append(f"{row['id']}: PDF ไม่ผ่าน - {', '.join(report['errors'])}")
    return {"checked": checked, "errors": errors}


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    manifest = project_root / "TOR_EXPERT_CURRENT_KNOWLEDGE" / "06_KNOWLEDGE_MANIFEST.csv"
    result = validate_manifest_files(manifest, project_root)
    print(f"ตรวจไฟล์ {result['checked']} รายการ")
    if result["errors"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("ไม่พบข้อผิดพลาดของไฟล์ที่ลงทะเบียน")
