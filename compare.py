import hashlib
import sys
import difflib
import re
import argparse
import os
import logging
import pymupdf
import pandas as pd
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
            logger.error(f"✘ Error reading .docx file '{path}': {e}", exc_info=True)
            sys.exit(1)
    elif path.lower().endswith(".txt"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                text_contents = f.read()
            f.close()
            return text_contents
        except OSError:
            print(f"✘ Error reading .txt file '{path}': {e}")
            logger.error(f"✘ Error reading .txt file '{path}': {e}")
            sys.exit(1)
    elif path.lower().endswith(".pdf"):
        with pymupdf.open(path) as f:
            text = chr(12).join([page.get_text() for page in f])
        return text
    elif path.lower().endswith(".xlsx"):
        try:
            df = pd.read_excel(path).fillna("")
            return df.to_csv(index=False)
        except Exception as e:
            print(f"✘ Error reading .xlsx file '{path}': {e}")
            logger.error(f"✘ Error reading .xlsx file '{path}': {e}", exc_info=True)
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
            logger.error(f"✘ Could not hash file {path}: {e}", exc_info=True)
            sys.exit(1)
    elif (
        path.lower().endswith(".txt")
        or path.lower().endswith(".pdf")
        or path.lower().endswith(".xlsx")
    ):
        try:
            sha256_hash = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            f.close()
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"✘ Could not hash file {path}: {e}")
            logger.error(f"✘ Could not hash file {path}: {e}", exc_info=True)
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


def compare(file_1: str, file_2: str, output_file: str | None) -> None:
    """
    Perform Line and Word-Level Comparison for .txt or .docx.
    Args:
        file_1 (str): Path of First File for Comparison.
        file_2 (str): Path of Second File for Comparison.
    """
    print("⚠ Not identical.\nPerforming manual comparison...\n")
    logger.warning(f"{file_1} and {file_2} are not identical.")
    logger.info("Performing manual comparison.")

    if file_1.lower().endswith(".xlsx") and file_2.lower().endswith(".xlsx"):
        try:
            df1 = pd.read_excel(file_1).fillna("")
            df2 = pd.read_excel(file_2).fillna("")

            if df1.shape != df2.shape:
                print(
                    f"✘ {file_1} and {file_2} have different sizes.\nCalculating partial comparison..."
                )
                logger.warning(
                    f"✘ {file_1} and {file_2} have different sizes. Calculating partial comparison..."
                )

            diff = df1.compare(df2, result_names=(f"{file_1}", f"{file_2}"))

            total_cells = df1.size
            matching_cells = (df1.values == df2.values).sum()
            similarity = round((matching_cells / total_cells) * 100, 2)

            print(f"Differences between {file_1} and {file_2}: \n")
            print(diff)
            print(f"\nCell-level similarity: {similarity}%")

            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(f"Differences between {file_1} and {file_2}:\n")
                    f.write(diff.to_string())
                    f.write(f"\n\nCell-level similarity: {similarity}%\n")
                print(f"Output saved to {output_file}")

            logger.info(f"Excel comparison done. Cell-level similarity: {similarity}%")
            return
        except Exception as e:
            print(f"✘ Error comparing Excel files: {e}")
            logger.error(f"Error comparing Excel files: {e}", exc_info=True)
            return

    f1_text = read_text_from_file(file_1)
    f2_text = read_text_from_file(file_2)

    f1_lines = f1_text.splitlines()
    f2_lines = f2_text.splitlines()

    diff = difflib.unified_diff(f1_lines, f2_lines, fromfile=file_1, tofile=file_2)
    ratio_lines = round(
        difflib.SequenceMatcher(None, f1_lines, f2_lines).ratio() * 100, 2
    )
    f1_words = re.findall(r"\w+", f1_text.lower())
    f2_words = re.findall(r"\w+", f2_text.lower())
    ratio_words = round(
        difflib.SequenceMatcher(None, f1_words, f2_words).ratio() * 100, 2
    )

    print(f"Differences between {file_1} and {file_2}: \n")
    if output_file:
        try:
            with open(output_file, "w") as f:
                f.write(f"Differences between {file_1} and {file_2}: \n")
                for line in diff:
                    sys.stdout.write(line + "\n")
                    f.write(line + "\n")
                f.write("\nFinished manual comparison!")
                f.write(
                    f"\nLine-level similarity for {file_1} & {file_2}: {ratio_lines}%"
                )
                f.write(
                    f"\nWord-level similarity for {file_1} & {file_2}: {ratio_words}%"
                )
            f.close()
        except FileNotFoundError:
            print(f"✘ Output filepath: {f} does not exist.")
            logger.error(f"✘ Output filepath: {f} does not exist.", exc_info=True)
        except TypeError:
            print(f"✘ Data incompatible to write to file {f}")
            logger.error(f"✘ Data incompatible to write to file {f}", exc_info=True)
        except PermissionError:
            print(f"✘ Permission denied: Can't write to file: {f}")
            logger.error(
                f"✘ Permission denied: Can't write to file: {f}", exc_info=True
            )
        except IsADirectoryError:
            print(f"✘ Can't write to a directory! Given path: {f}")
            logger.error(
                f"✘ Can't write to a directory! Given path: {f}", exc_info=True
            )
        except OSError:
            print(f"✘ Something went wrong. Can't write to: {f}")
            logger.error(f"✘ System-level error. Can't write to: {f}", exc_info=True)
    else:
        for line in diff:
            sys.stdout.write(line + "\n")

    print("\nFinished manual comparison!")
    print(f"Line-level similarity: {ratio_lines}%")
    print(f"Word-level similarity: {ratio_words}%\n")
    print(f"Output has been saved to: {output_file}")

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
    OUTPUT_FILE = None

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
            help="<path_to_first_file> <path_to_second_file>",
        )
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            help="<path_to_output_file>",
            default="output.txt",
        )
        args = parser.parse_args()
        DOC_1, DOC_2 = args.file[0], args.file[1]
        OUTPUT_FILE = args.output

    except argparse.ArgumentError and TypeError:
        parser.print_help()
        sys.exit(2)

    if not os.path.exists(DOC_1) or not os.path.exists(DOC_2):
        print("✘ One or both file paths do not exist.")
        logger.error("✘ One or both file paths do not exist.", exc_info=True)
        sys.exit(2)

    if not DOC_1 or not DOC_2:
        print("✘ One or both file paths do not exist.")
        sys.exit(2)

    hashed_doc_1 = hash_docs(DOC_1)
    hashed_doc_2 = hash_docs(DOC_2)

    if not compare_hash(hashed_doc_1, hashed_doc_2, DOC_1, DOC_2):
        compare(DOC_1, DOC_2, OUTPUT_FILE)


if __name__ == "__main__":
    logger.info("Starting Program...")
    main(sys.argv[1:])
