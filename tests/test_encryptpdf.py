from unittest import TestCase

from encryptpdf import pipeline


class TestPdfFunction(TestCase):
    def test_pipeline(self):
        self.assertEquals("awesomePdfProtection", pipeline("awesomePdfProtection"))
