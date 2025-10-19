import hashlib
import sys
import difflib
import re
import getopt
import os
from docx import Document


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
            sys.exit(1)
    else:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except OSError:
            print(f"✘ Could not open/read text file: {path}")
            sys.exit(1)


def hash_docs(path: str) -> str:
    """
    Compute SHA-256 Hash of File Contents.
    Args:
        Path (str): Path of File.
    Returns:
        str: SHA-256 Hash of File Contents.
    """
    try:
        text = read_text_from_file(path)
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
    except Exception as e:
        print(f"✘ Could not hash file {path}: {e}")
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

    f1_text = read_text_from_file(file_1)
    f2_text = read_text_from_file(file_2)

    f1_lines = f1_text.splitlines()
    f2_lines = f2_text.splitlines()

    diff = difflib.unified_diff(f1_lines, f2_lines, fromfile=file_1, tofile=file_2)
    ratio_lines = round(difflib.SequenceMatcher(None, f1_lines, f2_lines).ratio() * 100, 2)

    print("Differences: \n")
    for line in diff:
        sys.stdout.write(line + "\n")

    print(f"\nFinished manual comparison!")
    print(f"Line-level similarity: {ratio_lines}%")

    f1_words = re.findall(r"\w+", f1_text.lower())
    f2_words = re.findall(r"\w+", f2_text.lower())
    ratio_words = round(difflib.SequenceMatcher(None, f1_words, f2_words).ratio() * 100, 2)

    print(f"Word-level similarity: {ratio_words}%\n")


def main(argv) -> None:
    """
    Main Function
    """
    DOC_1 = None
    DOC_2 = None

    try:
        opts, args = getopt.getopt(argv, "h", ["file1=", "file2="])
    except getopt.GetoptError:
        print("Usage: compare.py --file1=<path> --file2=<path>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Usage:\n  compare.py --file1=<path> --file2=<path>\n')
            sys.exit()
        elif opt == "--file1":
            DOC_1 = arg
        elif opt == "--file2":
            DOC_2 = arg

    if not DOC_1 or not DOC_2:
        print("✘ Both --file1 and --file2 are required.")
        sys.exit(2)

    if not os.path.exists(DOC_1) or not os.path.exists(DOC_2):
        print("✘ One or both file paths do not exist.")
        sys.exit(2)

    hashed_doc_1 = hash_docs(DOC_1)
    hashed_doc_2 = hash_docs(DOC_2)

    if not compare_hash(hashed_doc_1, hashed_doc_2, DOC_1, DOC_2):
        compare(DOC_1, DOC_2)


if __name__ == "__main__":
    main(sys.argv[1:])
