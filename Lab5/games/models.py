from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Game(models.Model):
    class Platform(models.TextChoices):
        PC = "PC", "PC"
        PLAYSTATION = "PS", "PlayStation"
        XBOX = "XBOX", "Xbox"
        NINTENDO = "NINTENDO", "Nintendo"
        MOBILE = "MOBILE", "Mobile"

    class Status(models.TextChoices):
        OWNED = "OWNED", "W kolekcji"
        WISHLIST = "WISHLIST", "Lista życzeń"
        COMPLETED = "COMPLETED", "Ukończona"
        ABANDONED = "ABANDONED", "Porzucona"

    # Pola z Lab 4
    title = models.CharField(max_length=150, verbose_name="Tytuł")
    genre = models.CharField(max_length=50, verbose_name="Gatunek")
    description = models.TextField(verbose_name="Opis gry")
    release_year = models.IntegerField(verbose_name="Rok premiery")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Ocena (1-10)"
    )
    available = models.BooleanField(default=True, verbose_name="Dostępna w kolekcji")
    added_date = models.DateField(auto_now_add=True, verbose_name="Data dodania do katalogu")

    # Nowe pola z Lab 5
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="Cena")
    decksup = models.BooleanField(default=False, verbose_name="Wsparcie na SteamOS")
    platform = models.CharField(
        max_length=20,
        choices=Platform.choices,
        default=Platform.PC,
        verbose_name="Platforma",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OWNED,
        verbose_name="Status kolekcji",
    )
    developer = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Studio / wydawca",
    )
    completion_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data ukończenia",
    )

    class Meta:
        verbose_name = "Gra"
        verbose_name_plural = "Gry"
        ordering = ["-release_year", "title"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "platform"],
                name="unique_game_title_platform",
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.release_year}, {self.get_platform_display()})"
