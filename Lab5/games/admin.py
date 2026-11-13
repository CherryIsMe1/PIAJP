from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "genre",
        "platform",
        "release_year",
        "rating",
        "status",
        "available",
        "price",
        "decksup",
        "completion_date",
        "added_date",
    )
    list_filter = ("status", "platform", "available", "decksup", "genre", "release_year")
    search_fields = ("title", "description", "genre", "developer")
    ordering = ("-release_year", "title")
    list_editable = ("status", "available", "decksup")
    list_per_page = 25
    date_hierarchy = "added_date"
    readonly_fields = ("added_date",)
    fieldsets = (
        (
            "Podstawowe informacje",
            {"fields": ("title", "genre", "developer", "description", "price", "decksup")},
        ),
        (
            "Wydanie i ocena",
            {"fields": ("release_year", "rating", "platform")},
        ),
        (
            "Kolekcja",
            {"fields": ("available", "status", "completion_date", "added_date")},
        ),
    )
