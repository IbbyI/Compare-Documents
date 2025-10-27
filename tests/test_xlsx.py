import tempfile
import unittest
import pandas as pd

from utils.reader import read_text_from_file


class TestDocxFileFunction(unittest.TestCase):
    def test_identical_Docx(self):
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as t1:
            path1 = t1.name
        df = pd.DataFrame({"A": ["Test Case."]})
        df.to_excel(path1, index=False)

        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as t2:
            path2 = t2.name
        df.to_excel(path2, index=False)

        file_1 = read_text_from_file(path1)
        file_2 = read_text_from_file(path2)

        self.assertEqual(file_1.strip(), file_2.strip())


if __name__ == "__main__":
    unittest.main()
