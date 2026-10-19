"""สร้าง ZIP จากโฟลเดอร์โดยรักษาชื่อไฟล์ภาษาไทยและโครงสร้างแบบพกพาได้"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path


def create_zip(source_directory: Path, destination: Path) -> None:
    """บีบอัดเนื้อหาภายในโฟลเดอร์โดยไม่เติมชื่อโฟลเดอร์ต้นทางลงใน ZIP"""
    source = source_directory.resolve(strict=True)
    target = destination.resolve()
    if not source.is_dir():
        raise NotADirectoryError(source)
    if target == source or source in target.parents:
        raise ValueError("ไฟล์ ZIP ปลายทางต้องอยู่นอกโฟลเดอร์ต้นทาง")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.unlink(missing_ok=True)
    with zipfile.ZipFile(
        target,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        allowZip64=True,
    ) as bundle:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                bundle.write(path, path.relative_to(source).as_posix())


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: create_zip.py SOURCE_DIRECTORY DESTINATION_ZIP", file=sys.stderr)
        return 2
    create_zip(Path(sys.argv[1]), Path(sys.argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
