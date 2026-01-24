from unittest import TestCase

from encryptpdf import pipeline


class TestPdfExample(TestCase):
    def test_pipeline_example(self):
        self.assertEqual("awesomePdfProtection", pipeline("awesomePdfProtection"))
