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

## Requirements

- Python 3.6+
- Python packages:
  - `python-docx`

Install dependencies using:

```bash
pip install python-docx
