import re
import sys
import difflib
import pandas as pd

from utils.reader import read_text_from_file
from utils.logger import log


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
        print(f"{doc1} and {doc2} Are Identical.\n")
        log(level="info", message=f"✔ {doc1} and {doc2} Are Identical.")
        log(level="info", message="Terminating Program.")
        return True
    return False


def compare_docs(file_1: str, file_2: str, output_file: str | None) -> None:
    """
    Perform Line and Word-Level Comparison for .txt or .docx.
    Args:
        file_1 (str): Path of First File for Comparison.
        file_2 (str): Path of Second File for Comparison.
    """
    print("⚠ Not Identical.\nPerforming Manual Comparison...\n")
    log(level="warning", message=f"{file_1} and {file_2} Are Not Identical.")
    log(level="info", message="Performing Manual Comparison.")

    if file_1.lower().endswith(".xlsx") and file_2.lower().endswith(".xlsx"):
        try:
            df1 = pd.read_excel(file_1).reset_index(drop=False)
            df2 = pd.read_excel(file_2).reset_index(drop=False)
            if df1.shape != df2.shape:
                print(
                    f"⚠ {file_1} and {file_2} Have Different Sizes.\nCalculating Partial Comparison..."
                )
                log(
                    level="warning",
                    message=f"⚠ {file_1} and {file_2} have different sizes. Calculating Partial comparison...",
                )

            diff = df1.compare(df2, result_names=(f"{file_1}", f"{file_2}")).fillna("")

            total_cells = df1.size
            matching_cells = (df1.values == df2.values).sum()
            similarity = round((matching_cells / total_cells) * 100, 2)

            print(f"Differences Between {file_1} and {file_2}: \n")
            print(diff)
            print(f"\nCell-level Similarity: {similarity}%")
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(f"Differences Between {file_1} and {file_2}:\n")
                    f.write(diff.to_string())
                    f.write(f"\n\nCell-level Similarity: {similarity}%\n")
                print(f"Output Saved To {output_file}")

            log(
                level="info",
                message=f"Excel Comparison Done. Cell-level Similarity: {similarity}%",
            )
            return
        except Exception as e:
            print(f"✘ Error Comparing Excel Files: {e}")
            log(
                level="error",
                message=f"✘ Error Comparing Excel Files: {e}",
                exc_info=True,
            )
            return

    f1_text = read_text_from_file(file_1)
    f2_text = read_text_from_file(file_2)

    f1_lines = f1_text.splitlines()
    f2_lines = f2_text.splitlines()

    difflib.unified_diff(f1_lines, f2_lines, fromfile=file_1, tofile=file_2)
    ratio_lines = round(
        difflib.SequenceMatcher(None, f1_lines, f2_lines).ratio() * 100, 2
    )
    f1_words = re.findall(r"\w+", f1_text.lower())
    f2_words = re.findall(r"\w+", f2_text.lower())
    ratio_words = round(
        difflib.SequenceMatcher(None, f1_words, f2_words).ratio() * 100, 2
    )

    print(f"Differences Between {file_1} and {file_2}: \n")
    if output_file:
        try:
            with open(output_file, "w") as f:
                f.write(f"Differences Between {file_1} and {file_2}: \n")
                for line in diff:
                    sys.stdout.write(line + "\n")
                    f.write(line + "\n")
                f.write("\nFinished Manual Comparison!")
                f.write(
                    f"\nLine-level Similarity for {file_1} & {file_2}: {ratio_lines}%"
                )
                f.write(
                    f"\nWord-level Similarity for {file_1} & {file_2}: {ratio_words}%"
                )
                f.close()
        except FileNotFoundError:
            print(f"✘ Output Filepath: {f} Does Not Exist.")
            log(
                level="error",
                message=f"✘ Output Filepath: {f} Does Not Exist.",
                exc_info=True,
            )
        except TypeError:
            print(f"✘ Data Incompatible to Write to File {f}")
            log(
                level="error",
                message=f"✘ Data Incompatible to Write to File {f}",
                exc_info=True,
            )
        except PermissionError:
            print(f"✘ Permission Denied: Can't Write to File: {f}")
            log(
                level="error",
                message=f"✘ Permission Denied: Can't Write to File: {f}",
                exc_info=True,
            )
        except IsADirectoryError:
            print(f"✘ Can't Write to a Directory! Given Path: {f}")
            log(
                level="error",
                message=f"✘ Can't Write to a Directory! Given Path: {f}",
                exc_info=True,
            )
        except OSError:
            print(f"✘ Something Went Wrong. Can't Write to: {f}")
            log(
                level="error",
                message=f"✘ System-Level Error. Can't Write To: {f}",
                exc_info=True,
            )
    else:
        for line in diff:
            sys.stdout.write(line + "\n")

    print("\nFinished Manual Comparison!")
    print(f"Line-level Similarity: {ratio_lines}%")
    print(f"Word-level Similarity: {ratio_words}%\n")
    print(f"Output Has Been Saved To: {output_file}")

    log(
        level="info",
        message=f"Line-Level Similarity For {file_1} & {file_2}: {ratio_lines}%",
    )
    log(
        level="info",
        message=f"Word-Level Similarity For {file_1} & {file_2}: {ratio_words}%",
    )
