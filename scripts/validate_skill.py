"""ตรวจ Skill ด้วย Python standard library เพื่อใช้ใน CI ได้โดยไม่พึ่งพา Codex ภายนอก"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def validate_skill(skill_directory: Path) -> list[str]:
    errors: list[str] = []
    entrypoint = skill_directory / "SKILL.md"
    if not entrypoint.exists():
        return [f"ไม่พบ {entrypoint}"]
    content = entrypoint.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        errors.append("SKILL.md ต้องมี YAML frontmatter")
        return errors
    end = content.find("\n---\n", 4)
    if end < 0:
        errors.append("YAML frontmatter ปิดไม่ครบ")
        return errors
    frontmatter = content[4:end].splitlines()
    fields: dict[str, str] = {}
    for line in frontmatter:
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    if fields.get("name") != skill_directory.name:
        errors.append("name ไม่ตรงกับชื่อโฟลเดอร์")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields.get("name", "")):
        errors.append("name ไม่เป็นรูปแบบ lowercase-kebab-case")
    if not fields.get("description"):
        errors.append("description ต้องมีค่า")
    if "TODO" in content or "TBD" in content:
        errors.append("พบ placeholder TODO/TBD")
    for reference in re.findall(r"(?:\(|`)((?:references/)[^)`]+)", content):
        if reference.startswith("references/knowledge/"):
            continue
        if not (skill_directory / reference).exists():
            errors.append(f"ไม่พบ reference: {reference}")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_skill.py SKILL_DIRECTORY", file=sys.stderr)
        return 2
    errors = validate_skill(Path(sys.argv[1]))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("SKILL_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
