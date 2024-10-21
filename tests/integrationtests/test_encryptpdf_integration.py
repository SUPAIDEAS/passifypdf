from unittest import TestCase

from encryptpdf import pipeline


class TestPdfIntegrationTests(TestCase):
    def test_pipeline_integration(self):
        self.assertEquals("awesomePdfProtection_IntegrationTest", pipeline("awesomePdfProtection_IntegrationTest"))
