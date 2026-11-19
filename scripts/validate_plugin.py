"""ตรวจ Plugin manifest และโครงสร้างขั้นพื้นฐาก่อนสร้างแพ็กเกจ"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "extensions",
}
REQUIRED_INTERFACE_FIELDS = {
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "brandColor",
    "defaultPrompt",
}


def validate_plugin_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"อ่าน manifest ไม่ได้: {exc}"]
    missing = REQUIRED_FIELDS - set(manifest)
    errors.extend(f"ขาดฟิลด์ระดับบน: {field}" for field in sorted(missing))
    if not isinstance(manifest.get("name"), str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", str(manifest.get("name", ""))
    ):
        errors.append("name ต้องเป็นตัวพิมพ์เล็กและขีดกลาง")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
        errors.append("version ต้องเป็นรูปแบบ major.minor.patch")
    if not isinstance(manifest.get("author"), dict) or not manifest["author"].get("name"):
        errors.append("author.name ต้องมีค่า")
    interface = manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
    errors.extend(
        f"ขาดฟิลด์ interface: {field}"
        for field in sorted(REQUIRED_INTERFACE_FIELDS - set(interface))
    )
    if manifest.get("$schema", "").startswith("https://") is False:
        errors.append("$schema ต้องเป็น HTTPS")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_plugin.py plugin.json", file=sys.stderr)
        return 2
    errors = validate_plugin_manifest(Path(sys.argv[1]))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PLUGIN_MANIFEST_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
