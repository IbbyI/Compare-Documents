import unittest
import tempfile
from utils.reader import read_text_from_file


class TestFileReaderFunction(unittest.TestCase):
    def test_identical_txt(self):
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".txt", delete=False
        ) as temp:
            temp.write("Test Case.")
            temp.flush()
            file_1 = read_text_from_file(temp.name)
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".txt", delete=False
        ) as temp:
            temp.write("Test Case.")
            temp.flush()
            file_2 = read_text_from_file(temp.name)
        self.assertEqual(file_1.strip(), file_2.strip())

    def test_different_txt(self):
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".txt", delete=False
        ) as temp:
            temp.write("Test Case.")
            temp.flush()
            file_1 = read_text_from_file(temp.name)
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".txt", delete=False
        ) as temp:
            temp.write("Hello World.")
            temp.flush()
            file_2 = read_text_from_file(temp.name)
        self.assertNotEqual(file_1.strip(), file_2.strip())


if __name__ == "__main__":
    unittest.main()
