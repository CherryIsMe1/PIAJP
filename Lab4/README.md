# Laboratorium 4: Samodzielna aplikacja Django API + JavaScript fetch()

Projekt zrealizowany w ramach przedmiotu Programowanie internetowe na Akademii im. Jakuba z Paradyża.

Aplikacja stanowi katalog gier wideo, łączący backend Django z asynchronicznym frontendem JavaScript wykorzystującym funkcję fetch() do pobierania danych w formacie JSON i manipulacji obiektami DOM bez konieczności przeładowywania strony.

## Tematyka i model danych

Model `Game` (aplikacja `katalog`) reprezentuje pozycję w katalogu gier.
Model spełnia wymóg min. 5 pól oraz min. 3 różnych typów pól (7 pól, 5 typów danych):

- `title` (`CharField(max_length=150)`) - Tytuł gry
- `genre` (`CharField(max_length=50)`) - Gatunek (np. RPG, Akcja, Strategia)
- `description` (`TextField`) - Opis fabuły i rozgrywki
- `release_year` (`IntegerField`) - Rok premiery gry
- `rating` (`IntegerField`) - Ocena w skali 1-10
- `available` (`BooleanField`) - Dostępność w bibliotece/kolekcji (True/False)
- `added_date` (`DateField`) - Data dodania wpisu do bazy (auto_now_add=True)

Metoda `__str__()` zwraca: `f"{self.title} ({self.release_year})"`.
Model jest zarejestrowany w panelu administracyjnym Django z filtrami i wyszukiwarką.

## Endpoint API i odpowiedź JSON

Aplikacja udostępnia endpointy:
- `/api/gry/` (główny endpoint)
- `/api/obiekty/` (alias)

### Parametry filtrowania (URL Query Params):
- `?available=true` - tylko dostępne gry
- `?available=false` - tylko niedostępne gry
- `?genre=RPG` - gry z wybranego gatunku
- `?search=wiedźmin` - wyszukiwanie w tytule i opisie

Filtrowanie odbywa się w bazie danych za pomocą Django ORM.

### Przykładowa struktura JSON:
```json
{
  "count": 8,
  "items": [
    {
      "id": 1,
      "title": "Wiedźmin 3: Dziki Gon",
      "genre": "RPG",
      "description": "Opis gry...",
      "release_year": 2015,
      "rating": 10,
      "available": true,
      "added_date": "2026-10-30"
    }
  ]
}
```

## Frontend i JavaScript fetch()

- Asynchroniczne pobieranie danych przyciskiem "Wczytaj dane" bez przeładowania strony.
- Sprawdzanie `response.ok` oraz parsowanie `response.json()`.
- Bezpieczna aktualizacja DOM za pomocą `document.createElement` i `textContent` (ochrona przed XSS).
- Obsługa stanów: komunikat o pobieraniu, pusta lista wyników, błędy połączenia.

## Uruchomienie lokalne

1. Aktywacja środowiska wirtualnego:
   ```bash
   source .venv/bin/activate
   ```
2. Uruchomienie serwera:
   ```bash
   python manage.py runserver
   ```
   Adres strony: `http://127.0.0.1:8000/`

## Panel administracyjny

- Adres: `http://127.0.0.1:8000/admin/`
- Login: `admin`
- Hasło: `admin123`
