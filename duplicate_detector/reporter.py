import json
from dataclasses import asdict

from .models import DuplicateGroup, DuplicateReport


def create_report(
    total_files_scanned: int,
    duplicate_groups: list[DuplicateGroup]
) -> DuplicateReport:

    total_duplicate_files = sum(
        len(group.files) for group in duplicate_groups
    )

    total_duplicate_size = sum(
        group.size * len(group.files)
        for group in duplicate_groups
    )

    return DuplicateReport(
        total_files_scanned=total_files_scanned,
        total_duplicate_files=total_duplicate_files,
        total_duplicate_groups=len(duplicate_groups),
        total_duplicate_size=total_duplicate_size,
        duplicate_groups=duplicate_groups
    )


def print_report(report: DuplicateReport) -> None:
    print("\nDuplicate File Report")
    print("=====================")

    print(f"Total files scanned       : {report.total_files_scanned}")
    print(f"Total duplicate files     : {report.total_duplicate_files}")
    print(f"Total duplicate groups    : {report.total_duplicate_groups}")
    print(f"Total disk space occupied : {report.total_duplicate_size} bytes")

    for index, group in enumerate(report.duplicate_groups, start=1):
        print(f"\nDuplicate Group {index}")
        print("-----------------")

        for file_path in group.files:
            print(file_path)


def save_json_report(report: DuplicateReport, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(asdict(report), file, indent=4)