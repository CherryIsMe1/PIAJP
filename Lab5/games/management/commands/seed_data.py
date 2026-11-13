from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from games.models import Game


class Command(BaseCommand):
    help = "Tworzy konto administratora i uzupełnia przykładowe dane katalogu gier."

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='Hubert').exists():
            User.objects.create_superuser('Hubert', '', '32037')
            self.stdout.write(self.style.SUCCESS("Utworzono konto administratora Hubert."))

        games_data = [
            {
                'title': 'Gorzów civ 12',
                'genre': 'Rts',
                'description': 'Gra typu Sid Civ',
                'release_year': 2024,
                'rating': 10,
                'available': True,
                'price': Decimal('49.99'),
                'decksup': True,
                'platform': Game.Platform.PC,
                'status': Game.Status.COMPLETED,
                'developer': 'Hubert Studio',
                'completion_date': date(2024, 12, 15),
            },
            {
                'title': 'Smawik The Hedgehog',
                'genre': 'Platformer',
                'description': 'Smawik biega po platformach',
                'release_year': 2023,
                'rating': 9,
                'available': True,
                'price': Decimal('19.99'),
                'decksup': True,
                'platform': Game.Platform.PC,
                'status': Game.Status.COMPLETED,
                'developer': 'Smawik Team',
                'completion_date': date(2023, 11, 2),
            },
            {
                'title': 'CyperPunk 2067',
                'genre': 'RPG',
                'description': 'Rpg w przyszłości',
                'release_year': 2020,
                'rating': 10,
                'available': True,
                'price': Decimal('199.99'),
                'decksup': True,
                'platform': Game.Platform.PC,
                'status': Game.Status.OWNED,
                'developer': 'CD Projekt Red',
                'completion_date': None,
            },
            {
                'title': 'Wiedźmin 3: Dziki Gon',
                'genre': 'RPG',
                'description': 'Biegasz z mieczem i szukasz Ciri',
                'release_year': 2015,
                'rating': 10,
                'available': True,
                'price': Decimal('99.99'),
                'decksup': True,
                'platform': Game.Platform.PC,
                'status': Game.Status.COMPLETED,
                'developer': 'CD Projekt Red',
                'completion_date': date(2024, 2, 10),
            },
            {
                'title': 'Elden Ring',
                'genre': 'Soulslike',
                'description': 'Turlanie się i bicie trudnych bossów',
                'release_year': 2022,
                'rating': 10,
                'available': True,
                'price': Decimal('249.99'),
                'decksup': True,
                'platform': Game.Platform.PLAYSTATION,
                'status': Game.Status.COMPLETED,
                'developer': 'FromSoftware',
                'completion_date': date(2024, 8, 20),
            },
            {
                'title': 'Red Dead Redemption 2',
                'genre': 'Akcja',
                'description': 'Kowboje, jazda konno i strzelanie',
                'release_year': 2018,
                'rating': 10,
                'available': True,
                'price': Decimal('159.99'),
                'decksup': True,
                'platform': Game.Platform.XBOX,
                'status': Game.Status.OWNED,
                'developer': 'Rockstar Games',
                'completion_date': None,
            },
            {
                'title': 'Hollow Knight',
                'genre': 'Metroidvania',
                'description': 'Skakanie małym robakiem pod ziemią',
                'release_year': 2017,
                'rating': 9,
                'available': False,
                'price': Decimal('59.99'),
                'decksup': True,
                'platform': Game.Platform.NINTENDO,
                'status': Game.Status.WISHLIST,
                'developer': 'Team Cherry',
                'completion_date': None,
            },
            {
                'title': 'Heroes of Might and Magic III',
                'genre': 'Strategia',
                'description': 'Zamki, smoki i tury na mapie',
                'release_year': 1999,
                'rating': 10,
                'available': True,
                'price': Decimal('39.99'),
                'decksup': False,
                'platform': Game.Platform.PC,
                'status': Game.Status.OWNED,
                'developer': 'New World Computing',
                'completion_date': None,
            },
            {
                'title': 'Hades',
                'genre': 'Roguelike',
                'description': 'Uciekanie z podziemi i umieranie',
                'release_year': 2020,
                'rating': 9,
                'available': False,
                'price': Decimal('89.99'),
                'decksup': True,
                'platform': Game.Platform.PC,
                'status': Game.Status.ABANDONED,
                'developer': 'Supergiant Games',
                'completion_date': None,
            },
            {
                'title': 'Minecraft',
                'genre': 'Sandbox',
                'description': 'Kopanie klocków i budowanie domków',
                'release_year': 2011,
                'rating': 9,
                'available': True,
                'price': Decimal('119.99'),
                'decksup': False,
                'platform': Game.Platform.PC,
                'status': Game.Status.OWNED,
                'developer': 'Mojang',
                'completion_date': None,
            },
        ]

        created = 0
        updated = 0
        for item in games_data:
            _, was_created = Game.objects.update_or_create(
                title=item['title'],
                defaults=item,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Dane gier: utworzono {created}, zaktualizowano {updated}."
        ))
