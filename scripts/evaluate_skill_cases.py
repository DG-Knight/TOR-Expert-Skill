"""ประเมินความครบถ้วนของ Skill และรูปแบบคำตอบแบบทำซ้ำได้"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def build_quality_report(results: list[dict[str, object]]) -> dict[str, object]:
    summary = Counter("passed" if result["passed"] else "failed" for result in results)
    summary["total"] = len(results)
    return {
        "summary": {
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
            "total": summary["total"],
        },
        "results": results,
    }


def evaluate_response(case: dict[str, object], response: str) -> dict[str, object]:
    missing: list[str] = []
    for term in [*case.get("required_sections", []), *case.get("required_terms", [])]:
        if term not in response:
            missing.append(str(term))
    forbidden = [str(term) for term in case.get("forbidden_terms", []) if term in response]
    return {
        "id": case["id"],
        "passed": not missing and not forbidden,
        "missing": missing,
        "forbidden": forbidden,
    }


def evaluate_skill(skill_directory: Path, fixture_path: Path) -> dict[str, object]:
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    files = {
        path.relative_to(skill_directory).as_posix(): path.read_text(encoding="utf-8")
        for path in skill_directory.rglob("*.md")
    }
    corpus = "\n".join(files.values())
    results: list[dict[str, object]] = []
    for case in fixture["skill_checks"]:
        missing_files = [name for name in case.get("required_files", []) if name not in files]
        missing_terms = [term for term in case.get("required_terms", []) if term not in corpus]
        results.append(
            {
                "id": case["id"],
                "passed": not missing_files and not missing_terms,
                "missing_files": missing_files,
                "missing_terms": missing_terms,
            }
        )
    return build_quality_report(results)


def main() -> int:
    parser = argparse.ArgumentParser(description="ประเมินคุณภาพเชิงนโยบายของ TOR Expert Skill")
    parser.add_argument("--skill", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = evaluate_skill(args.skill, args.fixture)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    print(output)
    return 0 if report["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
