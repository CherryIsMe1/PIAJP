# Laboratoria

Każdy projekt Django ma wydzieloną konfigurację projektu oraz osobne aplikacje:

- **Lab1** - Aplikacja Witaj (Django), aplikacja: `hello`
- **Lab2** - Strona Django (pliki statyczne/media)
- **Lab3** - Aplikacja Tasks / Zadania (Django), aplikacje: `frontend_demo`, `tasks`
- **Lab4** - Aplikacja - baza danych do gier, aplikacja: `games`

Struktura każdego projektu:

```text
LabN/
├── manage.py
├── LabN/          # settings.py, urls.py, asgi.py, wsgi.py
└── <aplikacja>/   # models.py, views.py, admin.py, urls.py, migrations/, templates/, static/
```
