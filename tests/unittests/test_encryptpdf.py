from unittest import TestCase
from unittest.mock import patch, mock_open
from passifypdf.encryptpdf import pipeline, encrypt_pdf


class TestPdfUnitTests(TestCase):
    def test_pipeline(self):
        self.assertEqual("awesomePdfProtection-UnitTest", pipeline("awesomePdfProtection-UnitTest"))

    @patch('passifypdf.encryptpdf.PdfReader')
    @patch('passifypdf.encryptpdf.PdfWriter')
    @patch('builtins.open', new_callable=mock_open)
    def test_encrypt_pdf(self, mock_file, mock_writer_cls, mock_reader_cls):
        # Setup mocks
        mock_reader_instance = mock_reader_cls.return_value
        mock_reader_instance.pages = ['page1', 'page2']
        
        mock_writer_instance = mock_writer_cls.return_value
        
        # Call the function
        encrypt_pdf("input.pdf", "output.pdf", "secret")
        
        # Verify PdfReader was called
        mock_reader_cls.assert_called_with("input.pdf")
        
        # Verify pages were added
        self.assertEqual(mock_writer_instance.add_page.call_count, 2)
        mock_writer_instance.add_page.assert_any_call('page1')
        mock_writer_instance.add_page.assert_any_call('page2')
        
        # Verify encryption
        mock_writer_instance.encrypt.assert_called_with("secret")
        
        # Verify file write
        mock_file.assert_called_with("output.pdf", "wb")
        mock_writer_instance.write.assert_called_with(mock_file())
