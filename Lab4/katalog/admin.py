from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "genre", "release_year", "rating", "available", "added_date")
    list_filter = ("available", "genre", "release_year")
    search_fields = ("title", "description", "genre")
    ordering = ("-release_year", "title")
