from unittest import TestCase

from encryptpdf import pipeline


class TestPdfUnitTests(TestCase):
    def test_pipeline(self):
        self.assertEquals("awesomePdfProtection-UnitTest", pipeline("awesomePdfProtection-UnitTest"))
