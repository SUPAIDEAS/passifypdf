"""Core PDF encryption module."""

import sys
from pathlib import Path
from typing import Union

from pypdf import PdfReader, PdfWriter


def encrypt_pdf(input_pdf: Union[str, Path], output_pdf: Union[str, Path], password: str) -> None:
    """
    Encrypts a PDF file with a password.

    Args:
        input_pdf (Union[str, Path]): Path to the input PDF file.
        output_pdf (Union[str, Path]): Path to the output PDF file.
        password (str): Password to encrypt the PDF with.

    Raises:
        FileNotFoundError: If the input PDF file does not exist.
        IsADirectoryError: If the input path is a directory.
        Exception: For other errors during processing.
    """
    input_path = Path(input_pdf)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file '{input_pdf}' not found.")

    if not input_path.is_file():
        raise IsADirectoryError(f"Input path '{input_pdf}' is not a file.")

    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Add all pages from the reader to the writer
        for page in reader.pages:
            writer.add_page(page)

        # Encrypt with a password
        writer.encrypt(password)

        # Write the encrypted PDF to a new PDF file passed as param
        with open(output_pdf, "wb") as f:
            writer.write(f)

    except Exception as e:
        raise Exception(f"Failed to encrypt PDF: {e}")


def main() -> None:
    """Entry point: delegates to the Typer CLI application."""
    from passifypdf.cli import app
    app()


if __name__ == "__main__":
    main()