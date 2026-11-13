from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Game

SORT_OPTIONS = {
    "title": ("title",),
    "-title": ("-title",),
    "rating": ("rating", "title"),
    "-rating": ("-rating", "title"),
    "release_year": ("release_year", "title"),
    "-release_year": ("-release_year", "title"),
    "added_date": ("added_date",),
    "-added_date": ("-added_date",),
    "price": ("price",),
    "-price": ("-price",),
    "decksup": ("decksup",),
    "-decksup": ("-decksup",),
}
DEFAULT_SORT = "-release_year"


def serialize_game(game):
    return {
        "id": game.id,
        "title": game.title,
        "genre": game.genre,
        "platform": game.platform,
        "platform_display": game.get_platform_display(),
        "status": game.status,
        "status_display": game.get_status_display(),
        "developer": game.developer,
        "description": game.description,
        "release_year": game.release_year,
        "rating": game.rating,
        "available": game.available,
        "price": str(game.price),
        "decksup": game.decksup,
        "completion_date": (
            game.completion_date.strftime("%Y-%m-%d")
            if game.completion_date
            else None
        ),
        "added_date": game.added_date.strftime("%Y-%m-%d") if game.added_date else "",
    }


def index(request):
    genres = Game.objects.values_list("genre", flat=True).distinct().order_by("genre")
    total_games = Game.objects.count()
    return render(request, "games/index.html", {
        "genres": genres,
        "total_games": total_games,
        "statuses": Game.Status.choices,
        "platforms": Game.Platform.choices,
    })


def api_games(request):
    # 1. ORM: pobranie wszystkich rekordów z sortowaniem (order_by)
    sort_param = request.GET.get("sort") or DEFAULT_SORT
    if sort_param not in SORT_OPTIONS:
        sort_param = DEFAULT_SORT
    games = Game.objects.all().order_by(*SORT_OPTIONS[sort_param])

    # 2. ORM: filtrowanie w bazie danych (filter)
    available_param = (request.GET.get("available") or "").strip().lower()
    if available_param in ("true", "1", "yes", "tak"):
        games = games.filter(available=True)
    elif available_param in ("false", "0", "no", "nie"):
        games = games.filter(available=False)

    decksup_param = (request.GET.get("decksup") or request.GET.get("DeckSup") or "").strip().lower()
    if decksup_param in ("true", "1", "yes", "tak"):
        games = games.filter(decksup=True)
    elif decksup_param in ("false", "0", "no", "nie"):
        games = games.filter(decksup=False)

    genre_param = request.GET.get("genre")
    if genre_param:
        games = games.filter(genre__iexact=genre_param.strip())

    status_param = (request.GET.get("status") or "").strip().upper()
    if status_param:
        games = games.filter(status=status_param)

    platform_param = (request.GET.get("platform") or "").strip().upper()
    if platform_param:
        games = games.filter(platform=platform_param)

    min_rating_param = request.GET.get("min_rating")
    if min_rating_param:
        try:
            min_rating = int(min_rating_param)
        except ValueError:
            return JsonResponse(
                {"error": "Parametr min_rating musi być liczbą całkowitą."},
                status=400,
            )
        games = games.filter(rating__gte=min_rating)

    search_param = request.GET.get("search")
    if search_param:
        phrase = search_param.strip()
        games = games.filter(
            Q(title__icontains=phrase)
            | Q(description__icontains=phrase)
            | Q(developer__icontains=phrase)
        )

    total = games.count()

    # 3. ORM: ograniczenie liczby wyników ([:limit])
    limit_param = request.GET.get("limit")
    if limit_param:
        try:
            limit = int(limit_param)
        except ValueError:
            return JsonResponse(
                {"error": "Parametr limit musi być liczbą całkowitą."},
                status=400,
            )
        if limit > 0:
            games = games[:limit]

    items = [serialize_game(game) for game in games]

    return JsonResponse({
        "count": total,
        "returned": len(items),
        "sort": sort_param,
        "items": items,
    })


def api_game_detail(request, pk):
    # 3. ORM: pobranie pojedynczego rekordu po ID (get)
    game = get_object_or_404(Game, pk=pk)
    return JsonResponse(serialize_game(game))


def api_stats(request):
    # Dodatkowe ORM: agregacja (aggregate) oraz first()
    summary = Game.objects.aggregate(
        total=Count("id"),
        available=Count("id", filter=Q(available=True)),
        average_rating=Avg("rating"),
    )
    by_status = list(
        Game.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )
    top_rated = Game.objects.order_by("-rating", "title").first()
    latest_added = Game.objects.order_by("-added_date", "-id").first()

    average_rating = summary["average_rating"]

    return JsonResponse({
        "total": summary["total"],
        "available": summary["available"],
        "average_rating": round(float(average_rating), 2) if average_rating is not None else None,
        "by_status": by_status,
        "top_rated": serialize_game(top_rated) if top_rated else None,
        "latest_added": serialize_game(latest_added) if latest_added else None,
    })
