import os
import sys
import argparse

from utils.comparison import *
from utils.logger import log


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
        print("✘ One or both file paths do not exist.")
        log(
            level="error",
            message="✘ One or both file paths do not exist.",
            exc_info=True,
        )
        sys.exit(2)

    if not DOC_1 or not DOC_2:
        print("✘ One or both file paths do not exist.")
        sys.exit(2)

    hashed_doc_1 = hash_docs(DOC_1)
    hashed_doc_2 = hash_docs(DOC_2)

    if not compare_hash(hashed_doc_1, hashed_doc_2, DOC_1, DOC_2):
        compare(DOC_1, DOC_2, OUTPUT_FILE)


if __name__ == "__main__":
    log(level="info", message="Starting Program...")
    main(sys.argv[1:])
