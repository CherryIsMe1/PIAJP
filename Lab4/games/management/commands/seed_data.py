from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from games.models import Game

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='Hubert').exists():
            User.objects.create_superuser('Hubert', '', '32037')

        games_data = [
            {
                'title': 'Gorzów civ 12',
                'genre': 'Rts',
                'description': 'Gra typu Sid Civ',
                'release_year': 2024,
                'rating': 10,
                'available': True,
            },
            {
                'title': 'Smawik The Hedgehog',
                'genre': 'Platformer',
                'description': 'Smawik biega po platformach',
                'release_year': 2023,
                'rating': 9,
                'available': True,
            },
            {
                'title': 'CyperPunk 2067',
                'genre': 'RPG',
                'description': 'Rpg w przyszłości',
                'release_year': 2020,
                'rating': 10,
                'available': True,
            },
            {
                'title': 'Wiedźmin 3: Dziki Gon',
                'genre': 'RPG',
                'description': 'Biegasz z mieczem i szukasz Ciri',
                'release_year': 2015,
                'rating': 10,
                'available': True,
            },
            {
                'title': 'Elden Ring',
                'genre': 'Soulslike',
                'description': 'Turlanie się i bicie trudnych bossów',
                'release_year': 2022,
                'rating': 10,
                'available': True,
            },
            {
                'title': 'Red Dead Redemption 2',
                'genre': 'Akcja',
                'description': 'Kowboje, jazda konno i strzelanie',
                'release_year': 2018,
                'rating': 10,
                'available': True,
            },
            {
                'title': 'Hollow Knight',
                'genre': 'Metroidvania',
                'description': 'Skakanie małym robakiem pod ziemią',
                'release_year': 2017,
                'rating': 9,
                'available': False,
            },
            {
                'title': 'Heroes of Might and Magic III',
                'genre': 'Strategia',
                'description': 'Zamki, smoki i tury na mapie',
                'release_year': 1999,
                'rating': 10,
                'available': True,
            },
            {
                'title': 'Hades',
                'genre': 'Roguelike',
                'description': 'Uciekanie z podziemi i umieranie',
                'release_year': 2020,
                'rating': 9,
                'available': False,
            },
            {
                'title': 'Minecraft',
                'genre': 'Sandbox',
                'description': 'Kopanie klocków i budowanie domków',
                'release_year': 2011,
                'rating': 9,
                'available': True,
            },
        ]

        for item in games_data:
            Game.objects.get_or_create(
                title=item['title'],
                defaults=item
            )
