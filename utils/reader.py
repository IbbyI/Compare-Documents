import sys
import pymupdf
from docx import Document
from pandas import read_excel, DataFrame

from .logger import log


def read_text_from_file(path: str) -> str | DataFrame:
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
            print(f"✘ Error Reading .docx File '{path}': {e}")
            log(
                level="error",
                message=f"✘ Error Reading .docx File '{path}': {e}",
                exc_info=True,
            )
            sys.exit(1)
    elif path.lower().endswith(".pdf"):
        with pymupdf.open(path) as f:
            text = chr(12).join([page.get_text() for page in f])
        return text
    elif path.lower().endswith(".xlsx"):
        try:
            df = read_excel(path)
            return df.to_csv(index=False)
        except Exception as e:
            print(f"✘ Error Reading .xlsx File '{path}': {e}")
            log(
                level="error",
                message=f"✘ Error Reading .xlsx File '{path}': {e}",
                exc_info=True,
            )
    else:
        try:
            with open(path, "r", encoding="utf-8") as f:
                text_contents = f.read()
                f.close()
            return text_contents
        except OSError:
            print(f"✘ Error Reading File '{path}': {e}")
            log(level="error", message=f"✘ Error Reading File '{path}': {e}")
            sys.exit(1)
