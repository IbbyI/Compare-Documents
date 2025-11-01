import os
import sys
import time
import argparse

from utils.hash import simple_hash, chunk_hash
from utils.logger import log
from utils.comparison import *


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
            description="""A Python script to compare two documents
            (.txt, .pdf, .xlsx, or .docx) for equality, line-level differences, 
            and word-level similarity.""",
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
        print("✘ One or Both File Paths Do Not Exist.")
        log(
            level="error",
            message="✘ One or Both File Paths Do Not Exist.",
            exc_info=True,
        )
        sys.exit(2)

    if not DOC_1 or not DOC_2:
        print("✘ One or Both File Paths Do Not Exist.")
        sys.exit(2)

    try:
        hashed_doc_1, hashed_doc_2 = chunk_hash(DOC_1), chunk_hash(DOC_2)
    except Exception as e:
        log(
            level="error",
            message=f"✘ Could Not Chunk Hash {DOC_1}, {DOC_2}",
            exc_info=True,
        )
        log(
            level="info",
            message=f"Attempting Simple Hash for {DOC_1}, {DOC_2}",
        )
        hashed_doc_1, hashed_doc_2 = simple_hash(DOC_1), simple_hash(DOC_2)

    if not compare_hash(hashed_doc_1, hashed_doc_2, DOC_1, DOC_2):
        compare_docs(DOC_1, DOC_2, OUTPUT_FILE)
        time_taken = round(time.time() - start_time, 2)
        print(f"Time Taken: {time_taken}s")
        log(level="info", message=f"Time Taken: {time_taken}s")


if __name__ == "__main__":
    start_time = time.time()
    log(level="info", message="Starting Program...")
    main(sys.argv[1:])
