from django.test import TestCase
from django.urls import reverse


class StaticDemoTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lab2')
