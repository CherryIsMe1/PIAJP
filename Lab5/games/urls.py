from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/gry/', views.api_games, name='api_gry'),
    path('api/gry/<int:pk>/', views.api_game_detail, name='api_gra'),
    path('api/obiekty/', views.api_games, name='api_obiekty'),
    path('api/statystyki/', views.api_stats, name='api_statystyki'),
]
