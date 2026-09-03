from pathlib import Path

from duplicate_detector.scanner import scan_directory

from unittest.mock import patch

def test_scan_directory(tmp_path):

    (tmp_path / "file1.txt").write_text("Sid")
    (tmp_path / "file2.txt").write_text("Hello")

    files = scan_directory(str(tmp_path))

    assert len(files) == 2

def test_symbolic_link_is_skipped(tmp_path):

    actual_file = tmp_path / "actual.txt"
    link_file = tmp_path / "link.txt"

    actual_file.write_text("content")

    try:
        link_file.symlink_to(actual_file)
    except (OSError, NotImplementedError):
        return

    files = scan_directory(str(tmp_path))

    paths = [file.path for file in files]

    assert str(actual_file) in paths
    assert str(link_file) not in paths

def test_permission_error_is_handled(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("content")

    with patch.object(
        type(file1),
        "stat",
        side_effect=PermissionError
    ):
        files = scan_directory(str(tmp_path))

    assert files == []

def test_file_not_found_error_is_handled(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("content")

    with patch.object(
        type(file1),
        "stat",
        side_effect=FileNotFoundError
    ):
        files = scan_directory(str(tmp_path))

    assert files == []


def test_file_disappears_during_scan(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("content")

    with patch.object(
        type(file1),
        "stat",
        side_effect=FileNotFoundError
    ):
        files = scan_directory(str(tmp_path))

    assert files == []

def test_os_error_is_handled(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("content")

    with patch.object(
        type(file1),
        "stat",
        side_effect=OSError
    ):
        files = scan_directory(str(tmp_path))

    assert files == []    