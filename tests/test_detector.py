from duplicate_detector.detector import find_duplicates
from duplicate_detector.models import FileInfo


def test_find_duplicates(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file3 = tmp_path / "unique.txt"

    file1.write_text("same content")
    file2.write_text("same content")
    file3.write_text("different")

    files = [
        FileInfo(path=file1, size=file1.stat().st_size),
        FileInfo(path=file2, size=file2.stat().st_size),
        FileInfo(path=file3, size=file3.stat().st_size),
    ]

    duplicates = find_duplicates(files)

    assert len(duplicates) == 1
    assert len(duplicates[0].files) == 2
    assert file1 in duplicates[0].files
    assert file2 in duplicates[0].files
    assert file3 not in duplicates[0].files

def test_empty_files_are_duplicates(tmp_path):
    file1 = tmp_path / "empty1.txt"
    file2 = tmp_path / "empty2.txt"

    file1.write_text("")
    file2.write_text("")

    files = [
        FileInfo(path=file1, size=file1.stat().st_size),
        FileInfo(path=file2, size=file2.stat().st_size),
    ]

    duplicates = find_duplicates(files)

    assert len(duplicates) == 1
    assert len(duplicates[0].files) == 2

from unittest.mock import patch


def test_different_size_files_are_not_hashed(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"

    file1.write_text("abc")
    file2.write_text("different content")

    files = [
        FileInfo(path=file1, size=file1.stat().st_size),
        FileInfo(path=file2, size=file2.stat().st_size),
    ]

    with patch(
        "duplicate_detector.detector.calculate_hash"
    ) as mock_hash:
        duplicates = find_duplicates(files)

    assert duplicates == []
    mock_hash.assert_not_called()    