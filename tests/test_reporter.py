import json

from duplicate_detector.models import DuplicateGroup
from duplicate_detector.reporter import (
    create_report,
    save_json_report
)


def test_create_report():
    duplicate_group = DuplicateGroup(
        checksum="abc123",
        size=3,
        files=[
            "file1.txt",
            "file2.txt"
        ]
    )

    report = create_report(
        total_files_scanned=3,
        duplicate_groups=[duplicate_group]
    )

    assert report.total_files_scanned == 3
    assert report.total_duplicate_files == 2
    assert report.total_duplicate_groups == 1
    assert report.total_duplicate_size == 6


def test_save_json_report(tmp_path):
    duplicate_group = DuplicateGroup(
        checksum="abc123",
        size=3,
        files=[
            "file1.txt",
            "file2.txt"
        ]
    )

    report = create_report(
        total_files_scanned=3,
        duplicate_groups=[duplicate_group]
    )

    output_file = tmp_path / "report.json"

    save_json_report(report, str(output_file))

    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["total_files_scanned"] == 3
    assert data["total_duplicate_files"] == 2
    assert data["total_duplicate_groups"] == 1
    assert data["total_duplicate_size"] == 6