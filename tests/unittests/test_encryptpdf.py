from unittest import TestCase
from unittest.mock import patch, mock_open
from passifypdf.encryptpdf import encrypt_pdf
import os
import shutil
import tempfile
from pypdf import PdfReader

class TestEncryptPdf(TestCase):
    """Unit tests for the encrypt_pdf function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_password = "test_password_123"
        self.temp_dir = tempfile.mkdtemp()
        self.input_pdf = os.path.join(
            os.path.dirname(__file__),
            "..",
            "resources",
            "Sample_PDF.pdf"
        )
        self.output_pdf = os.path.join(self.temp_dir, "encrypted_output.pdf")

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.output_pdf):
            os.remove(self.output_pdf)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_encrypt_pdf_creates_output_file(self):
        """Test that encrypt_pdf creates an output file."""
        encrypt_pdf(self.input_pdf, self.output_pdf, self.test_password)
        self.assertTrue(
            os.path.exists(self.output_pdf),
            "Encrypted PDF file should be created"
        )

    def test_encrypt_pdf_output_is_encrypted(self):
        """Test that the output PDF is actually encrypted."""
        encrypt_pdf(self.input_pdf, self.output_pdf, self.test_password)
        
        # Try to read without password - should indicate encryption
        reader = PdfReader(self.output_pdf)
        self.assertTrue(
            reader.is_encrypted,
            "Output PDF should be encrypted"
        )

    def test_encrypt_pdf_with_correct_password(self):
        """Test that encrypted PDF can be decrypted with correct password."""
        encrypt_pdf(self.input_pdf, self.output_pdf, self.test_password)
        
        reader = PdfReader(self.output_pdf)
        # Decrypt with correct password
        decrypt_result = reader.decrypt(self.test_password)
        
        self.assertNotEqual(
            decrypt_result,
            0,
            "Should be able to decrypt with correct password"
        )

    def test_encrypt_pdf_preserves_page_count(self):
        """Test that encryption preserves the number of pages."""
        # Read original page count
        original_reader = PdfReader(self.input_pdf)
        original_page_count = len(original_reader.pages)
        
        # Encrypt
        encrypt_pdf(self.input_pdf, self.output_pdf, self.test_password)
        
        # Read encrypted page count
        encrypted_reader = PdfReader(self.output_pdf)
        encrypted_reader.decrypt(self.test_password)
        encrypted_page_count = len(encrypted_reader.pages)
        
        self.assertEqual(
            original_page_count,
            encrypted_page_count,
            "Page count should be preserved after encryption"
        )

    def test_encrypt_pdf_with_invalid_input(self):
        """Test encrypt_pdf with non-existent input file."""
        non_existent_file = "non_existent_file.pdf"
        
        with self.assertRaises(FileNotFoundError):
            encrypt_pdf(non_existent_file, self.output_pdf, self.test_password)

    @patch('passifypdf.encryptpdf.PdfReader')
    @patch('passifypdf.encryptpdf.PdfWriter')
    @patch('passifypdf.encryptpdf.Path')  # Mock Path
    @patch('builtins.open', new_callable=mock_open)
    def test_encrypt_pdf(self, mock_file, mock_path_cls, mock_writer_cls, mock_reader_cls):
        # Setup mocks
        mock_path_instance = mock_path_cls.return_value
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True

        mock_reader_instance = mock_reader_cls.return_value
        mock_reader_instance.pages = ['page1', 'page2']
        
        mock_writer_instance = mock_writer_cls.return_value
        
        # Call the function
        encrypt_pdf("input.pdf", "output.pdf", "secret")
        
        # Verify Path existence check
        mock_path_cls.assert_called_with("input.pdf")
        mock_path_instance.exists.assert_called()
        mock_path_instance.is_file.assert_called()

        # Verify PdfReader was called with the path object
        mock_reader_cls.assert_called_with(mock_path_instance)
        
        # Verify pages were added
        self.assertEqual(mock_writer_instance.add_page.call_count, 2)
        mock_writer_instance.add_page.assert_any_call('page1')
        mock_writer_instance.add_page.assert_any_call('page2')
        
        # Verify encryption
        mock_writer_instance.encrypt.assert_called_with("secret")
        
        # Verify file write
        mock_file.assert_called_with("output.pdf", "wb")
        mock_writer_instance.write.assert_called_with(mock_file())

    @patch('passifypdf.encryptpdf.Path')
    def test_encrypt_pdf_file_not_found(self, mock_path_cls):
        mock_path_instance = mock_path_cls.return_value
        mock_path_instance.exists.return_value = False
        
        with self.assertRaises(FileNotFoundError):
            encrypt_pdf("nonexistent.pdf", "output.pdf", "secret")

    @patch('passifypdf.encryptpdf.Path')
    def test_encrypt_pdf_is_directory(self, mock_path_cls):
        mock_path_instance = mock_path_cls.return_value
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = False
        
        with self.assertRaises(IsADirectoryError):
            encrypt_pdf("directory", "output.pdf", "secret")

    @patch('passifypdf.encryptpdf.get_arg_parser')
    @patch('passifypdf.encryptpdf.encrypt_pdf')
    @patch('passifypdf.encryptpdf.Path')
    @patch('builtins.print')
    def test_main_with_force_flag(self, mock_print, mock_path_cls, mock_encrypt_pdf, mock_arg_parser):
        """Test main() with --force flag when output file exists."""
        mock_parser_instance = mock_arg_parser.return_value
        mock_args = type('Args', (), {'input': 'in.pdf', 'output': 'out.pdf', 'passwd': 'pass', 'force': True})()
        mock_parser_instance.parse_args.return_value = mock_args

        mock_path_instance = mock_path_cls.return_value
        mock_path_instance.exists.return_value = True

        from passifypdf.encryptpdf import main
        result = main()

        self.assertEqual(result, 0)
        mock_encrypt_pdf.assert_called_with('in.pdf', 'out.pdf', 'pass')
        mock_path_cls.assert_called_with('out.pdf')

    @patch('passifypdf.encryptpdf.get_arg_parser')
    @patch('passifypdf.encryptpdf.encrypt_pdf')
    @patch('passifypdf.encryptpdf.Path')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_main_without_force_flag_user_says_yes(self, mock_input, mock_print, mock_path_cls, mock_encrypt_pdf, mock_arg_parser):
        """Test main() without --force flag, user agrees to overwrite."""
        mock_parser_instance = mock_arg_parser.return_value
        mock_args = type('Args', (), {'input': 'in.pdf', 'output': 'out.pdf', 'passwd': 'pass', 'force': False})()
        mock_parser_instance.parse_args.return_value = mock_args

        mock_path_instance = mock_path_cls.return_value
        mock_path_instance.exists.return_value = True

        mock_input.return_value = 'y'

        from passifypdf.encryptpdf import main
        result = main()

        self.assertEqual(result, 0)
        mock_encrypt_pdf.assert_called_with('in.pdf', 'out.pdf', 'pass')
        mock_path_cls.assert_called_with('out.pdf')

    @patch('passifypdf.encryptpdf.get_arg_parser')
    @patch('passifypdf.encryptpdf.encrypt_pdf')
    @patch('passifypdf.encryptpdf.Path')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_main_without_force_flag_user_says_no(self, mock_input, mock_print, mock_path_cls, mock_encrypt_pdf, mock_arg_parser):
        """Test main() without --force flag, user refuses to overwrite."""
        mock_parser_instance = mock_arg_parser.return_value
        mock_args = type('Args', (), {'input': 'in.pdf', 'output': 'out.pdf', 'passwd': 'pass', 'force': False})()
        mock_parser_instance.parse_args.return_value = mock_args

        mock_path_instance = mock_path_cls.return_value
        mock_path_instance.exists.return_value = True

        mock_input.return_value = 'n'

        from passifypdf.encryptpdf import main
        result = main()

        self.assertEqual(result, 0)
        mock_encrypt_pdf.assert_not_called()
        mock_print.assert_called_with("Operation cancelled.")
        mock_path_cls.assert_called_with('out.pdf')

    @patch('passifypdf.encryptpdf.get_arg_parser')
    @patch('passifypdf.encryptpdf.encrypt_pdf')
    @patch('passifypdf.encryptpdf.Path')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_main_without_force_flag_file_not_exists(self, mock_input, mock_print, mock_path_cls, mock_encrypt_pdf, mock_arg_parser):
        """Test main() without --force flag when output file does not exist."""
        mock_parser_instance = mock_arg_parser.return_value
        mock_args = type('Args', (), {'input': 'in.pdf', 'output': 'out.pdf', 'passwd': 'pass', 'force': False})()
        mock_parser_instance.parse_args.return_value = mock_args

        mock_path_instance = mock_path_cls.return_value
        mock_path_instance.exists.return_value = False

        from passifypdf.encryptpdf import main
        result = main()

        self.assertEqual(result, 0)
        mock_encrypt_pdf.assert_called_with('in.pdf', 'out.pdf', 'pass')
        mock_path_cls.assert_called_with('out.pdf')
        mock_input.assert_not_called()
