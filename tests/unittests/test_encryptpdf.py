from unittest import TestCase
from unittest.mock import patch, mock_open
from passifypdf.encryptpdf import encrypt_pdf


class TestPdfUnitTests(TestCase):

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
