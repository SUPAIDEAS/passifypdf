from unittest import TestCase

from encryptpdf import pipeline


class TestPdfUnitTests(TestCase):
    def test_pipeline(self):
        self.assertEquals("awesomePdfProtection-UnitTest", pipeline("awesomePdfProtection-UnitTest"))


from encryptpdf import encrypt_pdf
import os
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
            os.rmdir(self.temp_dir)

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
