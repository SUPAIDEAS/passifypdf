from unittest import TestCase

from passifypdf.encryptpdf import pipeline


class TestPdfIntegrationTests(TestCase):
    def test_pipeline_integration(self):
        self.assertEqual("awesomePdfProtection-Integration", pipeline("awesomePdfProtection-Integration"))
