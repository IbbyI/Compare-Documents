import sys
import pymupdf
from docx import Document

from .logger import log


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
            log(
                level="error",
                message=f"✘ Error reading .docx file '{path}': {e}",
                exc_info=True,
            )
            sys.exit(1)
    elif path.lower().endswith(".txt"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                text_contents = f.read()
                f.close()
            return text_contents
        except OSError:
            print(f"✘ Error reading .txt file '{path}': {e}")
            log(level="error", message=f"✘ Error reading .txt file '{path}': {e}")
            sys.exit(1)
    elif path.lower().endswith(".pdf"):
        with pymupdf.open(path) as f:
            text = chr(12).join([page.get_text() for page in f])
        return text
    elif path.lower().endswith(".xlsx"):
        try:
            import pandas as pd

            df = pd.read_excel(path)
            return df.to_csv(index=False)
        except Exception as e:
            print(f"✘ Error reading .xlsx file '{path}': {e}")
            log(
                level="error",
                message=f"✘ Error reading .xlsx file '{path}': {e}",
                exc_info=True,
            )
    else:
        sys.exit(f"✘ Unsupported file type: {path}")
