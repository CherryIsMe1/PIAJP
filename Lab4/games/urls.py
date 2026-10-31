from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/gry/', views.api_games, name='api_gry'),
    path('api/obiekty/', views.api_games, name='api_obiekty'),
]
