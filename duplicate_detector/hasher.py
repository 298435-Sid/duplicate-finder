import hashlib


def calculate_hash(file_path: str, chunk_size: int = 1024 * 1024) -> str:
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()