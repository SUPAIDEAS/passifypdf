import argparse
from unittest import TestCase
from unittest.mock import patch
from passifypdf.cli import get_arg_parser

class TestCli(TestCase):
    """Unit tests for the cli module."""

    @patch("passifypdf.cli.version")
    def test_get_arg_parser_with_version(self, mock_version):
        """Test argument parser when package version is found."""
        mock_version.return_value = "1.2.3"
        parser = get_arg_parser()
        
        # We can test if the --version flag is handled correctly by capturing exit and stdout
        with patch('sys.stdout') as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                parser.parse_args(["--version"])
            self.assertEqual(cm.exception.code, 0)
            
        # Unfortunately, argparse action='version' prints directly to stdout/sys.stdout.
        # So we can't easily assert on the exact printed string here if argparse handles it natively,
        # but we can verify the version is added to the format string.
        # As an alternative, we know version is used inside get_arg_parser:
        # arg_parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
        has_version_action = any(action.dest == 'version' for action in parser._actions)
        self.assertTrue(has_version_action)

    @patch("passifypdf.cli.version")
    def test_get_arg_parser_without_version(self, mock_version):
        """Test argument parser when package is not installed (PackageNotFoundError)."""
        from importlib.metadata import PackageNotFoundError
        mock_version.side_effect = PackageNotFoundError()
        parser = get_arg_parser()
        
        with patch('sys.stdout') as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                parser.parse_args(["--version"])
            self.assertEqual(cm.exception.code, 0)
            
        has_version_action = any(action.dest == 'version' for action in parser._actions)
        self.assertTrue(has_version_action)
