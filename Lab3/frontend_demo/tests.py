from django.test import TestCase, Client
from django.urls import reverse

class FrontendDemoViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'frontend_demo/index.html')

    def test_index_view_contains_expected_content(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Witamy w aplikacji Django!')
