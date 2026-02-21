# passifypdf
Use passifypdf to protect your PDF files with a password of your choice. 
Same as encrypt or lock your PDF via a password.

## Before & After:
<img width="1534" alt="Pasted Graphic 100" src="https://github.com/user-attachments/assets/ee2ead62-6480-4312-af8b-762ec240cc10">

# How to use ?

## Clone
```bash
git clone https://github.com/SUPAIDEAS/passifypdf.git
```

## Install Dependencies
Uses [`uv`](https://github.com/astral-sh/uv) for dependency management.

```bash
cd passifypdf
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

## Usage
Run the CLI tool using `uv run`:

```bash
uv run passifypdf --help
```

Or install into a virtual environment and use directly:
```bash
uv sync
.venv/bin/passifypdf --help
```


Sample Run:
```bash
passifypdf -i input.pdf -o protected.pdf -p mySecretPassword

# -------------------------Sample output----------------------
# Congratulations!
# PDF file encrypted successfully and saved as 'protected.pdf'
```

## Known Issues
If you have any special chars (example: an emoji like Star 🌟) in the PDF file, it gives a minor complaint during execution.
But it still does the job, so you can ignore that "char or object error" which you see in the output.

## Programmatic Usage (Python API)

You can also use `passifypdf` directly from your Python scripts:

```python
from passifypdf.encryptpdf import encrypt_pdf

# Encrypt a PDF file with a password
encrypt_pdf(
    input_pdf="path/to/input.pdf",
    output_pdf="path/to/protected.pdf",
    password="mySecretPassword",
)
```

The `encrypt_pdf` function raises `FileNotFoundError` if the input file does not exist,
`IsADirectoryError` if the path points to a directory, and `Exception` for other
encryption failures.

## Note:
In general you can use passifypdf to protect your PDF files against chance attackers.
But you should not rely on this for mission-critical data or situations.

## Build & Run Locally
Visit [BUILD.md](BUILD.md)