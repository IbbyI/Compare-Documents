import sys
import hashlib

from utils.reader import read_text_from_file
from utils.logger import log

file_contents = None


def simple_hash(path: str) -> str:
    """
    Compute SHA-256 Hash of File Contents After Saving to Memory.
    Args:
        path (str): Path of File
    Returns:
        str: SHA-256 Hashof File Contents
    """
    try:
        file_contents = read_text_from_file(path)
        log(level="info", message=f"Simple Hashing Contents from File {path}.")
        return hashlib.sha256(file_contents.encode("utf-8")).hexdigest()
    except Exception as e:
        log(level="error", message=f"Error Hashing Contents from File {path}")
        return


def chunk_hash(path: str) -> str:
    """
    Compute SHA-256 Hash of File Contents in 4KB Chunks.
    Args:
        path (str): Path of File
    Returns:
        str: SHA-256 Hash of File Contents
    """
    try:
        log(level="info", message=f"Chunk Hashing Contents from File {path}.")
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
            f.close()
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"✘ Could Not Hash File {path}: {e}")
        log(
            level="error",
            message=f"✘ Could Not Hash File {path}: {e}",
            exc_info=True,
        )
        sys.exit(1)
