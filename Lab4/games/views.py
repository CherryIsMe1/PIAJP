from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Game

def index(request):
    genres = Game.objects.values_list('genre', flat=True).distinct().order_by('genre')
    total_games = Game.objects.count()
    return render(request, 'games/index.html', {
        'genres': genres,
        'total_games': total_games,
    })

def api_games(request):
    games = Game.objects.all()

    available_param = request.GET.get('available')
    if available_param is not None and available_param != '':
        if available_param.lower() in ('true', '1', 'yes', 'tak'):
            games = games.filter(available=True)
        elif available_param.lower() in ('false', '0', 'no', 'nie'):
            games = games.filter(available=False)

    genre_param = request.GET.get('genre')
    if genre_param:
        games = games.filter(genre__iexact=genre_param.strip())

    search_param = request.GET.get('search')
    if search_param:
        games = games.filter(
            Q(title__icontains=search_param.strip()) |
            Q(description__icontains=search_param.strip())
        )

    items = []
    for g in games:
        items.append({
            'id': g.id,
            'title': g.title,
            'genre': g.genre,
            'description': g.description,
            'release_year': g.release_year,
            'rating': g.rating,
            'available': g.available,
            'added_date': g.added_date.strftime('%Y-%m-%d') if g.added_date else '',
        })

    return JsonResponse({
        'count': len(items),
        'items': items,
    })
