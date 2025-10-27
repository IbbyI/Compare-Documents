import tempfile
import unittest
import pymupdf

from utils.reader import read_text_from_file


class TestDocxFileFunction(unittest.TestCase):
    def test_identical_Docx(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as t1:
            path1 = t1.name
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Test Case.")
        doc.save(path1)
        doc.close()

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as t2:
            path2 = t2.name
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Test Case.")
        doc.save(path2)
        doc.close()

        file_1 = read_text_from_file(path1)
        file_2 = read_text_from_file(path2)

        self.assertEqual(file_1.strip(), file_2.strip())


if __name__ == "__main__":
    unittest.main()
