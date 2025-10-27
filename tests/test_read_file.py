import unittest
import tempfile
from utils.reader import read_text_from_file

class TestFileReaderFunction(unittest.TestCase):
    def test_reader(self):
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".txt", delete=False) as temp:
            temp.write("Test Case.")
            temp.flush()
            result = read_text_from_file(temp.name)
            self.assertEqual(result.strip(), "Test Case.")

if __name__ == "__main__":
    unittest.main()
