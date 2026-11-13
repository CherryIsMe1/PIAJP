# Laboratorium 5: Modele, migracje i operacje ORM

Projekt zrealizowany w ramach przedmiotu Programowanie internetowe na Akademii im. Jakuba z Paradyża.

Laboratorium 5 rozwija aplikację katalogu gier z Laboratorium 4. Model `Game` został rozbudowany o nowe pola, wykonano migracje, rozszerzono panel administracyjny oraz dodano zapytania ORM (filtrowanie, sortowanie, pobieranie pojedynczego rekordu i agregacje) wykorzystywane przez endpointy JSON.

## Struktura projektu

```text
Lab5/
├── manage.py
├── Lab5/                      # konfiguracja projektu
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── games/                     # aplikacja Django
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    ├── management/commands/seed_data.py
    ├── templates/games/
    └── static/games/
```

## Model danych

Model `Game` (aplikacja `games`) po rozbudowie ma **11 pól i 6 różnych typów danych**.

Pola z Laboratorium 4:

- `title` (`CharField(max_length=150)`) - Tytuł gry
- `genre` (`CharField(max_length=50)`) - Gatunek (np. RPG, Akcja, Strategia)
- `description` (`TextField`) - Opis fabuły i rozgrywki
- `release_year` (`IntegerField`) - Rok premiery gry
- `rating` (`IntegerField`) - Ocena w skali 1-10
- `available` (`BooleanField(default=True)`) - Dostępność w bibliotece/kolekcji
- `added_date` (`DateField(auto_now_add=True)`) - Data dodania wpisu do bazy

Nowe pola dodane w Laboratorium 5:

- `platform` (`CharField(max_length=20, choices=Platform.choices, default="PC")`) - Platforma: PC, PlayStation, Xbox, Nintendo, Mobile
- `status` (`CharField(max_length=20, choices=Status.choices, default="OWNED")`) - Status kolekcji: w kolekcji, lista życzeń, ukończona, porzucona
- `developer` (`CharField(max_length=100, blank=True, default="")`) - Studio / wydawca
- `completion_date` (`DateField(null=True, blank=True)`) - Data ukończenia (może być pusta)
- `price` (`DecimalField(max_digits=6, decimal_places=2, default=0.00)`) - Cena gry
- `decksup` (`BooleanField(default=False)`) - Wsparcie dla SteamOS (Steam Deck)

Dodatkowo:

- `UniqueConstraint(fields=["title", "platform"], name="unique_game_title_platform")` - ta sama gra nie może być dwukrotnie dodana na tę samą platformę.
- `__str__()` zwraca czytelną reprezentację: `f"{self.title} ({self.release_year}, {self.get_platform_display()})"`.

## Migracje

Po zmianach w modelu wykonano:

```bash
python manage.py makemigrations
python manage.py migrate
```

Powstały migracje:
1. `games/migrations/0002_game_completion_date_game_developer_game_platform_and_more.py` - platforma, status, developer, data ukończenia i ograniczenie unikalności.
2. `games/migrations/0003_game_decksup_game_price_alter_game_rating.py` - dodanie ceny (`price`), wsparcia SteamOS (`decksup`) oraz walidacji oceny (1-10).

Stan migracji można sprawdzić poleceniem:

```bash
python manage.py makemigrations --check --dry-run   # "No changes detected"
python manage.py migrate --check
```

## Panel administracyjny

Panel jest dostępny pod adresem `http://127.0.0.1:8000/admin/`.

Konfiguracja `GameAdmin`:

- `list_display` - wszystkie nowe pola (`platform`, `status`, `completion_date`) obok dotychczasowych,
- `list_filter` - filtry po `status`, `platform`, `available`, `genre`, `release_year`,
- `search_fields` - wyszukiwanie także po `developer`,
- `list_editable` - szybka zmiana `status` i `available` z listy rekordów,
- `date_hierarchy` - nawigacja po dacie dodania,
- `fieldsets` - formularz edycji pogrupowany w sekcje: podstawowe informacje, wydanie i ocena, kolekcja,
- `added_date` jest tylko do odczytu.

Dane startowe (10 rekordów, wszystkie z uzupełnionymi nowymi polami) tworzy polecenie:

```bash
python manage.py seed_data
```

Polecenie używa `update_or_create`, więc można je uruchamiać wielokrotnie - istniejące rekordy zostaną uzupełnione, a nie zduplikowane.

## Operacje ORM

Zapytania znajdują się w `games/views.py`:

1. **Sortowanie** (`order_by`) - parametr `?sort=`:

   ```python
   games = Game.objects.all().order_by(*SORT_OPTIONS[sort_param])
   ```

2. **Filtrowanie** (`filter`) - parametry `?available=`, `?genre=`, `?status=`, `?platform=`, `?min_rating=`, `?search=`:

   ```python
   games = games.filter(status="COMPLETED")
   games = games.filter(rating__gte=9)
   games = games.filter(Q(title__icontains=phrase) | Q(developer__icontains=phrase))
   ```

3. **Ograniczenie wyników** (`[:N]`) - parametr `?limit=`:

   ```python
   games = games[:3]
   ```

4. **Pojedynczy rekord** (`get` / `first`) - endpoint szczegółów oraz statystyki:

   ```python
   game = get_object_or_404(Game, pk=pk)
   top_rated = Game.objects.order_by("-rating", "title").first()
   ```

5. **Agregacje** (`aggregate`, `annotate`) - endpoint statystyk:

   ```python
   summary = Game.objects.aggregate(
       total=Count("id"),
       available=Count("id", filter=Q(available=True)),
       average_rating=Avg("rating"),
   )
   by_status = Game.objects.values("status").annotate(count=Count("id"))
   ```

Wszystkie filtry i sortowanie wykonuje baza danych - frontend nie pobiera całej tabeli i nie filtruje w JavaScript.

## Endpointy API

- `/api/gry/` lub `/games/api/gry/` - lista gier (JSON),
- `/api/gry/<id>/` lub `/games/api/gry/<id>/` - pojedyncza gra,
- `/api/obiekty/` - alias listy gier,
- `/api/statystyki/` - agregacje i rekordy `first()`.

### Parametry listy gier

| Parametr | Przykład | Działanie |
| --- | --- | --- |
| `sort` | `?sort=-rating` | Sortowanie ORM (`title`, `-title`, `rating`, `-rating`, `release_year`, `-release_year`, `added_date`, `-added_date`) |
| `available` | `?available=true` | Tylko dostępne/niedostępne |
| `genre` | `?genre=RPG` | Gatunek (bez rozróżniania wielkości liter) |
| `status` | `?status=COMPLETED` | Status kolekcji |
| `platform` | `?platform=PS` | Platforma |
| `min_rating` | `?min_rating=9` | Minimalna ocena |
| `search` | `?search=wiedźmin` | Szukanie w tytule, opisie i studiu |
| `limit` | `?limit=3` | Ograniczenie liczby wyników (`[:N]`) |

Przykład:

```text
/api/gry/?genre=RPG&status=COMPLETED&sort=-rating&limit=3
```

Odpowiedź zawiera `count` (liczba po filtrach), `returned` (liczba zwróconych rekordów), `sort` oraz listę `items`. Każdy rekord ma m.in. `id`, `title`, `genre`, `platform`, `status`, `developer`, `release_year`, `rating`, `available`, `completion_date` i `added_date`.

## Frontend

Frontend z Laboratorium 4 nadal korzysta z endpointu `/api/gry/` i został rozszerzony o:

- filtry `status` i `platform`,
- wybór sortowania (rok, ocena, tytuł, data dodania),
- prezentację nowych pól: platformy, statusu kolekcji, studia i daty ukończenia,
- podgląd aktualnie budowanego adresu API.

Dane są nadal wstawiane do DOM przez `document.createElement` i `textContent` (ochrona przed XSS).

## Uruchomienie lokalne

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

- Strona: `http://127.0.0.1:8000/` lub `http://127.0.0.1:8000/games/`
- API: `http://127.0.0.1:8000/api/gry/`
- Statystyki: `http://127.0.0.1:8000/api/statystyki/`
- Panel administracyjny: `http://127.0.0.1:8000/admin/`
- Login: `Hubert`
- Hasło: `32037`

## Publikacja na PythonAnywhere

1. Wypchnij zmiany do repozytorium Git:

   ```bash
   git add Lab5
   git commit -m "Laboratorium 5: rozbudowa modelu, migracje i ORM"
   git push
   ```

2. W konsoli Bash na PythonAnywhere pobierz zmiany:

   ```bash
   cd ~/PIAJP
   git pull
   ```

3. Zainstaluj zależności i wykonaj migracje w środowisku wirtualnym:

   ```bash
   source ~/.virtualenvs/<nazwa-venv>/bin/activate
   pip install -r Lab5/requirements.txt
   cd Lab5
   python manage.py migrate
   python manage.py seed_data
   ```

4. W zakładce **Web** ustaw katalog roboczy, plik WSGI i ścieżkę do `staticfiles`, a następnie kliknij **Reload**.
5. Sprawdź stronę, `/api/gry/`, `/api/gry/1/`, `/api/statystyki/` oraz panel admina.
