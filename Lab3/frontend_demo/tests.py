from django.test import TestCase, Client
from django.urls import reverse

class FrontendDemoTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_template_used(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'frontend_demo/index.html')

    def test_index_content(self):
        response = self.client.get(reverse('index'))
        content = response.content.decode('utf-8')
        self.assertIn('Moja aplikacja Django', content)
        self.assertIn('Witamy w aplikacji Django!', content)
        self.assertIn('Strona główna', content)
        self.assertIn('O nas', content)
        self.assertIn('Kontakt', content)
        self.assertIn('Podstawy frontendu', content)
        self.assertIn('To jest przykładowa strona wykorzystująca HTML i CSS w Django.', content)
        self.assertIn('Jan Kowalski', content)
        self.assertIn('/static/frontend_demo/style.css', content)
