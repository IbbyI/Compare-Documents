# Document Comparison Tool

A Python script to compare two text or Word (`.txt` or `.docx`) documents for equality, line-level differences, and word-level similarity.

---

## Features

- Supports both `.txt` and `.docx` files.
- Computes SHA-256 hash to quickly detect identical files.
- Provides detailed manual comparison if files differ:
  - Line-level differences.
  - Word-level similarity percentage.
- Command-line interface for easy use.

---

## Prerequisites
Ensure that you have the following dependencies installed:

- **Python 3.x**
- **Required Python packages**: Install required packages using `pip`:
```bash
pip install -r requirements.txt
```
## How to Use

```bash
python compare.py --file1=<path_to_first_file> --file2=<path_to_second_file>
```

### Example

```bash
python compare.py --file1=document1.docx --file2=document2.txt
```
If files are identical, the output looks like:

```bash
✔ Finished Comparison!
document1.docx and document2.txt are identical.
```

If the files are not identical, the output looks like:
```bash
⚠ Not identical.
Performing manual comparison...

Differences:
--- document1.docx
+++ document2.txt
@@ -1,3 +1,3 @@
-This is the first document.
+This is the second document.

Finished manual comparison!
Line-level similarity: 85.71%
Word-level similarity: 90.32%
```
## Contributing
Feel free to fork this project, submit issues, or contribute improvements via pull requests.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Author
This project was created by [Ibby](https://github.com/IbbyI).