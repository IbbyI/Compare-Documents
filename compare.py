import hashlib
import sys
import difflib
import re
import argparse
import os
import logging
from docx import Document

FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(
    format=FORMAT, filename="compare.log", filemode="w", level=logging.INFO
)
logger = logging.getLogger(__name__)


def read_text_from_file(path: str) -> str:
    """
    Return Plain Text From Either .txt or .docx File.
    Args:
        path: Path of file.
    Returns:
        str: Plain Text Stripped From .txt or .docx File.
    """
    if path.lower().endswith(".docx"):
        try:
            doc = Document(path)
            text = []
            for para in doc.paragraphs:
                text.append(para.text)
            return "\n".join(text)
        except Exception as e:
            print(f"✘ Error reading .docx file '{path}': {e}")
            logger.error(f"✘ Error reading .docx file '{path}': {e}")
            sys.exit(1)
    elif path.lower().endswith(".txt"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except OSError:
            print(f"✘ Error reading .txt file '{path}': {e}")
            logger.error(f"✘ Error reading .txt file '{path}': {e}")
            sys.exit(1)
    else:
        sys.exit(f"✘ Unsupported file type: {path}")


def hash_docs(path: str) -> str:
    """
    Compute SHA-256 Hash of File Contents.
    Args:
        Path (str): Path of File.
    Returns:
        str: SHA-256 Hash of File Contents.
    """
    if path.lower().endswith(".docx"):
        try:
            text = read_text_from_file(path)
            logger.info(f"Hashing Text from file: {path}")
            return hashlib.sha256(text.encode("utf-8")).hexdigest()
        except Exception as e:
            print(f"✘ Could not hash file {path}: {e}")
            logger.error(f"✘ Could not hash file {path}: {e}")
            sys.exit(1)
    elif path.lower().endswith(".txt"):
        try:
            sha256_hash = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"✘ Could not hash file {path}: {e}")
            logger.error(f"✘ Could not hash file {path}: {e}")
            sys.exit(1)


def compare_hash(hash1: str, hash2: str, doc1: str, doc2: str) -> bool:
    """
    Compare hash values.
    Args:
        hash1 (str): Hash of First File.
        hash2 (str): Hash of Second FIle.
        doc1 (str): Path of First File for Comparison.
        doc2 (str): Path of Second File for Comparison.
    Returns:
        bool: Returns True if hash1 == hash2, Else Returns False.
    """
    if hash1 == hash2:
        print("✔ Finished Comparison!")
        print(f"{doc1} and {doc2} are identical.\n")
        logger.info(f"{doc1} and {doc2} are identical.")
        logger.info("Terminating Program.")
        return True
    return False


def compare(file_1: str, file_2: str) -> None:
    """
    Perform Line and Word-Level Comparison for .txt or .docx.
    Args:
        file_1 (str): Path of First File for Comparison.
        file_2 (str): Path of Second File for Comparison.
    """
    print("⚠ Not identical.\nPerforming manual comparison...\n")
    logger.warning(f"{file_1} and {file_2} are not identical.")
    logger.info("Performing manual comparison.")

    f1_text = read_text_from_file(file_1)
    f2_text = read_text_from_file(file_2)

    f1_lines = f1_text.splitlines()
    f2_lines = f2_text.splitlines()

    diff = difflib.unified_diff(f1_lines, f2_lines, fromfile=file_1, tofile=file_2)
    ratio_lines = round(
        difflib.SequenceMatcher(None, f1_lines, f2_lines).ratio() * 100, 2
    )

    print("Differences: \n")
    for line in diff:
        sys.stdout.write(line + "\n")

    print(f"\nFinished manual comparison!")
    print(f"Line-level similarity: {ratio_lines}%")

    f1_words = re.findall(r"\w+", f1_text.lower())
    f2_words = re.findall(r"\w+", f2_text.lower())
    ratio_words = round(
        difflib.SequenceMatcher(None, f1_words, f2_words).ratio() * 100, 2
    )

    print(f"Word-level similarity: {ratio_words}%\n")

    logger.info(f"Line-level similarity for {file_1} & {file_2}: {ratio_lines}%")
    logger.info(f"Word-level similarity for {file_1} & {file_2}: {ratio_words}%")


def main(argv: list[str]) -> None:
    """
    Main Function
    Args:
        argv list[str]: User Arguments When Launching Program.
    """
    DOC_1 = None
    DOC_2 = None

    try:
        parser = argparse.ArgumentParser(
            prog="compare",
            description="""A Python script to compare two text or Word 
            (.txt or .docx) documents for equality, line-level differences, 
            and word-level similarity.\n""",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument(
            "-f",
            "--file",
            type=str,
            nargs=2,
            help="<path_to_first_file>, <path_to_second_file>",
        )
        args = parser.parse_args()
        DOC_1, DOC_2 = args.file[0], args.file[1]
    except argparse.ArgumentError and TypeError:
        parser.print_help()
        sys.exit(2)

    if not os.path.exists(DOC_1) or not os.path.exists(DOC_2):
        print("✘ One or both file paths do not exist.")
        logger.error("✘ One or both file paths do not exist.")
        sys.exit(2)

    hashed_doc_1 = hash_docs(DOC_1)
    hashed_doc_2 = hash_docs(DOC_2)

    if not compare_hash(hashed_doc_1, hashed_doc_2, DOC_1, DOC_2):
        compare(DOC_1, DOC_2)


if __name__ == "__main__":
    logger.info("Starting Program...")
    main(sys.argv[1:])
