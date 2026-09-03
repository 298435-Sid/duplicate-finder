from collections import defaultdict
from typing import List

from .hasher import calculate_hash
from .models import DuplicateGroup, FileInfo


def find_duplicates(files: List[FileInfo]) -> List[DuplicateGroup]:
    
    size_groups = defaultdict(list)

    for file in files:
        size_groups[file.size].append(file)

    duplicate_groups = []

    for size, candidates in size_groups.items():

        if len(candidates) < 2:
            continue

        hash_groups = defaultdict(list)

        for file in candidates:
            try:
                checksum = calculate_hash(file.path)
                hash_groups[checksum].append(file.path)

            except (PermissionError, FileNotFoundError, OSError):
                continue

        for checksum, paths in hash_groups.items():

            if len(paths) > 1:
                duplicate_groups.append(
                    DuplicateGroup(
                        checksum=checksum,
                        size=size,
                        files=paths
                    )
                )

    return duplicate_groups