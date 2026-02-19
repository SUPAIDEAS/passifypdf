import os
from unittest import TestCase

from pypdf import PdfReader, PdfWriter

from passifypdf.encryptpdf import encrypt_pdf


class TestPdfIntegrationTests(TestCase):
    def setUp(self):
        self.input_pdf = "test_input.pdf"
        self.output_pdf = "test_output.pdf"
        self.password = "strongpassword"

        # Create a dummy PDF
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        with open(self.input_pdf, "wb") as f:
            writer.write(f)

    def tearDown(self):
        # Cleanup files
        if os.path.exists(self.input_pdf):
            os.remove(self.input_pdf)
        if os.path.exists(self.output_pdf):
            os.remove(self.output_pdf)

    def test_encrypt_pdf_integration(self):
        # Encrypt the PDF
        encrypt_pdf(self.input_pdf, self.output_pdf, self.password)

        # Verify output exists
        self.assertTrue(os.path.exists(self.output_pdf))

        # Verify it is encrypted
        reader = PdfReader(self.output_pdf)
        self.assertTrue(reader.is_encrypted)

        # Verify we can decrypt it
        self.assertTrue(reader.decrypt(self.password))
        self.assertEqual(len(reader.pages), 1)
