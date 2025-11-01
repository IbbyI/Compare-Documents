[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Cross--platform-green)](#)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)](#)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

# 🧾 Document Comparison Tool

A powerful and efficient **Python-based CLI utility** for comparing two documents — checking equality, identifying line-level differences, and computing word- or cell-level similarity.

---

## ✨ Features

- 🔍 Supports multiple file types (`.txt`, `.docx`, `.xlsx`, etc.)
- ⚡ Fast comparison using **SHA-256 hashing**
  - Files are hashed in 4KB chunks for optimal memory use
- 📄 Provides detailed comparisons when files differ:
  - Line-level and word-level differences
  - Cell-level comparison for spreadsheets
- 💻 Simple **command-line interface** for quick use

---

## 🧰 Prerequisites

Ensure the following are installed:

- **Python 3.x**
- Required dependencies (install via `pip`):

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the comparison with:

```bash
python compare.py -f <path_to_first_file> <path_to_second_file> -o <path_to_output_file>
```

> 💡 The `-o` flag is optional. If omitted, output defaults to `output.txt`.

---

## 🧩 Example Outputs

### ✅ Identical Files

```bash
✔ Finished Comparison!
document1.docx and document2.txt are identical.
```

---

### ⚠️ Non-Identical Files — `.docx` vs `.txt`

```bash
python compare.py -f document1.docx document2.txt
```

Output:

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
Time Taken: 0.12s
```

---

### ⚠️ Non-Identical Files — `.xlsx` vs `.xlsx`

```bash
python compare.py -f document1.xlsx document2.xlsx
```

Output:

```bash
⚠ Not identical.
Performing manual comparison...

Differences between document1.xlsx and document2.xlsx:

              C1                            C2                            C3
  document1.xlsx document2.xlsx document1.xlsx document2.xlsx document1.xlsx document2.xlsx
0             55             42           12.0           17.0           13.0           65.0
1             73             21           11.0           64.0
2             13             55                                         55.0           33.0
3             74             63
4             84             22           63.0           52.0           71.0           19.0

Cell-level similarity: 56.0%
Output saved to output.txt
Time taken: 0.20s
```

> Blank cells indicate identical content.

---

## 💾 Saving Results

You can save comparison results to a file using the `-o` or `--output` flag:

```bash
python compare.py -f document1.docx document2.txt -o results.txt
```

- If files differ → saves differences and similarity metrics
- If files are identical → saves a confirmation message
- Default output file (if `-o` not used): **output.txt**

> ⚠ Existing `output.txt` files **will be overwritten**.

---

## 🤝 Contributing

Contributions are welcome!
Feel free to:

- Fork the repository
- Submit issues or feature requests
- Open pull requests with improvements

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

Created by [**Ibby**](https://github.com/IbbyI)


