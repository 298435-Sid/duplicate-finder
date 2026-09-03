from dataclasses import dataclass
from typing import List


@dataclass
class FileInfo:
    path: str
    size: int


@dataclass
class DuplicateGroup:
    checksum: str
    size: int
    files: List[str]


@dataclass
class DuplicateReport:
    total_files_scanned: int
    total_duplicate_files: int
    total_duplicate_groups: int
    total_duplicate_size: int
    duplicate_groups: List[DuplicateGroup]