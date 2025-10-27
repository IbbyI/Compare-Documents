import re
import sys
import hashlib
import difflib
import pandas as pd

from utils.reader import read_text_from_file
from .logger import log


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
            log(level="info", message=f"Hashing Text from file: {path}")
            return hashlib.sha256(text.encode("utf-8")).hexdigest()
        except Exception as e:
            print(f"✘ Could not hash file {path}: {e}")
            log(
                level="error",
                message=f"✘ Could not hash file {path}: {e}",
                exc_info=True,
            )
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
            log(
                level="error",
                message=f"✘ Could not hash file {path}: {e}",
                exc_info=True,
            )
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
        log(level="info", message=f"{doc1} and {doc2} are identical.")
        log(level="info", message="Terminating Program.")
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
    log(level="warning", message=f"{file_1} and {file_2} are not identical.")
    log(level="info", message="Performing manual comparison.")

    if file_1.lower().endswith(".xlsx") and file_2.lower().endswith(".xlsx"):
        try:
            df1 = pd.read_excel(file_1).reset_index(drop=False)
            df2 = pd.read_excel(file_2).reset_index(drop=False)
            if df1.shape != df2.shape:
                print(
                    f"✘ {file_1} and {file_2} have different sizes.\nCalculating partial comparison..."
                )
                log.warning(
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

            log(
                level="info",
                message=f"Excel comparison done. Cell-level similarity: {similarity}%",
            )
            return
        except Exception as e:
            print(f"✘ Error comparing Excel files: {e}")
            log(
                level="error",
                message=f"Error comparing Excel files: {e}",
                exc_info=True,
            )
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
            log.error(f"✘ Output filepath: {f} does not exist.", exc_info=True)
        except TypeError:
            print(f"✘ Data incompatible to write to file {f}")
            log.error(f"✘ Data incompatible to write to file {f}", exc_info=True)
        except PermissionError:
            print(f"✘ Permission denied: Can't write to file: {f}")
            log.error(f"✘ Permission denied: Can't write to file: {f}", exc_info=True)
        except IsADirectoryError:
            print(f"✘ Can't write to a directory! Given path: {f}")
            log.error(f"✘ Can't write to a directory! Given path: {f}", exc_info=True)
        except OSError:
            print(f"✘ Something went wrong. Can't write to: {f}")
            log.error(f"✘ System-level error. Can't write to: {f}", exc_info=True)
    else:
        for line in diff:
            sys.stdout.write(line + "\n")

    print("\nFinished manual comparison!")
    print(f"Line-level similarity: {ratio_lines}%")
    print(f"Word-level similarity: {ratio_words}%\n")
    print(f"Output has been saved to: {output_file}")

    log(
        level="info",
        message=f"Line-level similarity for {file_1} & {file_2}: {ratio_lines}%",
    )
    log(
        level="info",
        message=f"Word-level similarity for {file_1} & {file_2}: {ratio_words}%",
    )
