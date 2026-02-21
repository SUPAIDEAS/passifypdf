"""CLI module using Typer for the passifypdf tool."""

import logging
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import typer
from typing_extensions import Annotated

from passifypdf.encryptpdf import encrypt_pdf

logger = logging.getLogger(__name__)

try:
    __version__ = version("passifypdf")
except PackageNotFoundError:
    __version__ = "unknown"

app = typer.Typer(
    name="passifypdf",
    help="Encrypt a PDF file with a password of your choice.",
    epilog="For more information, visit: https://github.com/SUPAIDEAS/passifypdf",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Print the version and exit."""
    if value:
        typer.echo(f"passifypdf {__version__}")
        raise typer.Exit()


@app.command()
def encrypt(
    input: Annotated[
        Path,
        typer.Option(
            "--input", "-i",
            help="Path to the input PDF file to be encrypted.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    output: Annotated[
        Path,
        typer.Option(
            "--output", "-o",
            help="Path where the encrypted PDF file will be saved.",
        ),
    ],
    passwd: Annotated[
        str,
        typer.Option(
            "--passwd", "-p",
            help="Password to encrypt the PDF file with.",
        ),
    ],
    force: Annotated[
        bool,
        typer.Option(
            "--force", "-f",
            help="Overwrite the output file if it already exists without prompting.",
        ),
    ] = False,
    version: Annotated[
        bool,
        typer.Option(
            "--version", "-v",
            help="Show the version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Encrypt a PDF file with a password of your choice."""

    if output.exists() and not force:
        overwrite = typer.confirm(
            f"File '{output}' already exists. Overwrite?",
            default=False,
        )
        if not overwrite:
            logger.info("Operation cancelled.")
            raise typer.Exit()

    try:
        encrypt_pdf(input, output, passwd)
        logger.info(
            "Congratulations!\nPDF file encrypted successfully and saved as '%s'",
            output,
        )
    except Exception as e:
        logger.error("Error: %s", e)
        raise typer.Exit(code=1)


def get_typer_app() -> typer.Typer:
    """Return the configured Typer application instance."""
    return app