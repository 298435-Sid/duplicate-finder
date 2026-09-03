from pathlib import Path
from typing import List

from .models import FileInfo


def scan_directory(directory: str) -> List[FileInfo]:
    files = []

    root = Path(directory)

    for path in root.rglob("*"):
        try:
            if path.is_symlink():
                continue

            if path.is_file():
                size = path.stat().st_size
                files.append(FileInfo(
                    path=str(path),
                    size=size
                ))

        except (PermissionError, FileNotFoundError, OSError):
            continue

    # print(f"Total files found: {len(files)}")    
    # for file in files:
    #     print(file.path)

    return files

