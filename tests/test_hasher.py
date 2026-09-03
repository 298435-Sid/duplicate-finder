from duplicate_detector.hasher import calculate_hash


def test_same_content_same_hash(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"

    file1.write_text("content")
    file2.write_text("content")

    hash1 = calculate_hash(str(file1))
    hash2 = calculate_hash(str(file2))

    assert hash1 == hash2


def test_different_content_different_hash(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"

    file1.write_text("content1")
    file2.write_text("content2")

    hash1 = calculate_hash(str(file1))
    hash2 = calculate_hash(str(file2))

    assert hash1 != hash2


def test_large_file(tmp_path):
    file = tmp_path / "large_file.txt"

    content = b"A" * (2 * 1024 * 1024)
    file.write_bytes(content)

    checksum = calculate_hash(str(file))

    assert checksum
    assert len(checksum) == 64