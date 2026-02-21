"""Unit tests for the Typer-based CLI module."""

from pathlib import Path
from typing import Generator
from unittest import TestCase
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from passifypdf.cli import app


class TestTyperCli(TestCase):
    """Tests for the Typer CLI application."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.runner = CliRunner()

    # ------------------------------------------------------------------
    # --help
    # ------------------------------------------------------------------

    def test_help_flag(self) -> None:
        """Test that --help exits 0 and mentions key options."""
        result = self.runner.invoke(app, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("--input", result.output)
        self.assertIn("--output", result.output)
        self.assertIn("--passwd", result.output)

    # ------------------------------------------------------------------
    # --version
    # ------------------------------------------------------------------

    def test_version_flag(self) -> None:
        """Test that --version exits 0 and prints the version."""
        result = self.runner.invoke(app, ["--version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("passifypdf", result.output)

    # ------------------------------------------------------------------
    # Happy path
    # ------------------------------------------------------------------

    @patch("passifypdf.cli.encrypt_pdf")
    def test_encrypt_success(self, mock_encrypt: MagicMock) -> None:
        """Test a successful encryption invocation."""
        with self.runner.isolated_filesystem():
            # Create a dummy input file so Typer's `exists=True` check passes
            Path("input.pdf").write_bytes(b"%PDF-1.4 dummy")
            result = self.runner.invoke(
                app,
                [
                    "--input", "input.pdf",
                    "--output", "output.pdf",
                    "--passwd", "secret",
                    "--force",
                ],
            )
        self.assertEqual(result.exit_code, 0)
        mock_encrypt.assert_called_once()

    # ------------------------------------------------------------------
    # Output collision — --force bypasses prompt
    # ------------------------------------------------------------------

    @patch("passifypdf.cli.encrypt_pdf")
    def test_force_flag_skips_prompt(self, mock_encrypt: MagicMock) -> None:
        """--force skips the overwrite prompt when output already exists."""
        with self.runner.isolated_filesystem():
            Path("input.pdf").write_bytes(b"%PDF-1.4 dummy")
            Path("output.pdf").write_bytes(b"existing")
            result = self.runner.invoke(
                app,
                [
                    "--input", "input.pdf",
                    "--output", "output.pdf",
                    "--passwd", "secret",
                    "--force",
                ],
            )
        self.assertEqual(result.exit_code, 0)
        mock_encrypt.assert_called_once()

    # ------------------------------------------------------------------
    # Output collision — user says no
    # ------------------------------------------------------------------

    @patch("passifypdf.cli.encrypt_pdf")
    def test_no_force_user_declines(self, mock_encrypt: MagicMock) -> None:
        """Without --force, declining the prompt should cancel the operation."""
        with self.runner.isolated_filesystem():
            Path("input.pdf").write_bytes(b"%PDF-1.4 dummy")
            Path("output.pdf").write_bytes(b"existing")
            # Provide 'n' as user input to the prompt
            result = self.runner.invoke(
                app,
                [
                    "--input", "input.pdf",
                    "--output", "output.pdf",
                    "--passwd", "secret",
                ],
                input="n\n",
            )
        self.assertEqual(result.exit_code, 0)
        mock_encrypt.assert_not_called()

    # ------------------------------------------------------------------
    # Output collision — user says yes
    # ------------------------------------------------------------------

    @patch("passifypdf.cli.encrypt_pdf")
    def test_no_force_user_accepts(self, mock_encrypt: MagicMock) -> None:
        """Without --force, accepting the prompt should proceed with encryption."""
        with self.runner.isolated_filesystem():
            Path("input.pdf").write_bytes(b"%PDF-1.4 dummy")
            Path("output.pdf").write_bytes(b"existing")
            result = self.runner.invoke(
                app,
                [
                    "--input", "input.pdf",
                    "--output", "output.pdf",
                    "--passwd", "secret",
                ],
                input="y\n",
            )
        self.assertEqual(result.exit_code, 0)
        mock_encrypt.assert_called_once()

    # ------------------------------------------------------------------
    # Missing required options
    # ------------------------------------------------------------------

    def test_missing_required_options(self) -> None:
        """Omitting required options should exit with a non-zero code."""
        result = self.runner.invoke(app, [])
        self.assertNotEqual(result.exit_code, 0)

    # ------------------------------------------------------------------
    # Non-existent input file
    # ------------------------------------------------------------------

    def test_input_file_not_found(self) -> None:
        """Passing a non-existent input file should exit with an error."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(
                app,
                [
                    "--input", "ghost.pdf",
                    "--output", "output.pdf",
                    "--passwd", "secret",
                ],
            )
        self.assertNotEqual(result.exit_code, 0)

    # ------------------------------------------------------------------
    # encrypt_pdf raises an error
    # ------------------------------------------------------------------

    @patch("passifypdf.cli.encrypt_pdf")
    def test_encrypt_failure_exits_with_1(self, mock_encrypt: MagicMock) -> None:
        """If encrypt_pdf raises an exception, CLI should exit with code 1."""
        mock_encrypt.side_effect = Exception("boom")
        with self.runner.isolated_filesystem():
            Path("input.pdf").write_bytes(b"%PDF-1.4 dummy")
            result = self.runner.invoke(
                app,
                [
                    "--input", "input.pdf",
                    "--output", "output.pdf",
                    "--passwd", "secret",
                    "--force",
                ],
            )
        self.assertEqual(result.exit_code, 1)

    # ------------------------------------------------------------------
    # get_typer_app helper
    # ------------------------------------------------------------------

    def test_get_typer_app_returns_app(self) -> None:
        """get_typer_app() should return the configured Typer instance."""
        from passifypdf.cli import get_typer_app
        result = get_typer_app()
        self.assertIs(result, app)
