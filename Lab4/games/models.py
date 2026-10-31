from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=150, verbose_name="Tytuł")
    genre = models.CharField(max_length=50, verbose_name="Gatunek")
    description = models.TextField(verbose_name="Opis gry")
    release_year = models.IntegerField(verbose_name="Rok premiery")
    rating = models.IntegerField(verbose_name="Ocena (1-10)")
    available = models.BooleanField(default=True, verbose_name="Dostępna w kolekcji")
    added_date = models.DateField(auto_now_add=True, verbose_name="Data dodania do katalogu")

    class Meta:
        verbose_name = "Gra"
        verbose_name_plural = "Gry"
        ordering = ["-release_year", "title"]

    def __str__(self):
        return f"{self.title} ({self.release_year})"
