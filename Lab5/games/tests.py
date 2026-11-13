from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from games.models import Game

class GameCatalogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.game1 = Game.objects.create(
            title="Wiedźmin 3",
            genre="RPG",
            description="Biegasz z mieczem i szukasz Ciri",
            release_year=2015,
            rating=10,
            available=True,
            price=Decimal("99.99"),
            decksup=True,
            platform=Game.Platform.PC,
        )
        self.game2 = Game.objects.create(
            title="Hades",
            genre="Roguelike",
            description="Uciekanie z podziemi i umieranie",
            release_year=2020,
            rating=9,
            available=False,
            price=Decimal("89.99"),
            decksup=False,
            platform=Game.Platform.PC,
        )

    def test_model_str(self):
        self.assertEqual(str(self.game1), "Wiedźmin 3 (2015, PC)")

    def test_model_fields(self):
        self.assertEqual(self.game1.title, "Wiedźmin 3")
        self.assertEqual(self.game1.genre, "RPG")
        self.assertTrue(self.game1.available)
        self.assertFalse(self.game2.available)
        self.assertEqual(self.game1.price, Decimal("99.99"))
        self.assertTrue(self.game1.decksup)
        self.assertFalse(self.game2.decksup)

    def test_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Katalog gier")

    def test_api_endpoint_returns_json(self):
        response = self.client.get(reverse('api_gry'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = response.json()
        self.assertIn('items', data)
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['items'][0]['price'], '89.99')
        self.assertIn('decksup', data['items'][0])

    def test_api_filter_available_true(self):
        response = self.client.get(reverse('api_gry') + '?available=true')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['title'], "Wiedźmin 3")
        self.assertTrue(data['items'][0]['available'])

    def test_api_filter_available_false(self):
        response = self.client.get(reverse('api_gry') + '?available=false')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['title'], "Hades")
        self.assertFalse(data['items'][0]['available'])

    def test_api_filter_decksup(self):
        response = self.client.get(reverse('api_gry') + '?decksup=true')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['title'], "Wiedźmin 3")

    def test_api_filter_genre(self):
        response = self.client.get(reverse('api_gry') + '?genre=RPG')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['genre'], "RPG")

    def test_api_obiekty_alias(self):
        response = self.client.get(reverse('api_obiekty'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['items']), 2)
