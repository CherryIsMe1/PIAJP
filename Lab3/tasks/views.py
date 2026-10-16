import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Task

@ensure_csrf_cookie
def index(request):
    """Widok główny renderujący interfejs TaskBoard."""
    return render(request, 'tasks/index.html')

def task_list_create(request):
    """
    GET /api/tasks/ - pobiera listę zadań.
    POST /api/tasks/ - tworzy nowe zadanie.
    """
    if request.method == 'GET':
        tasks = Task.objects.order_by('-created_at')
        return JsonResponse([task.to_dict() for task in tasks], safe=False, status=200)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
            return JsonResponse({'error': 'Nieprawidłowy format danych JSON.'}, status=400)

        title = data.get('title', '')
        if not isinstance(title, str) or not title.strip():
            return JsonResponse({'error': 'Treść zadania nie może być pusta.'}, status=400)

        task = Task.objects.create(title=title.strip())
        return JsonResponse(task.to_dict(), status=201)

    return HttpResponseNotAllowed(['GET', 'POST'])

def task_detail(request, task_id):
    """
    PATCH /api/tasks/<id>/ - aktualizuje status lub treść zadania.
    DELETE /api/tasks/<id>/ - usuwa zadanie.
    """
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': f'Zadanie o ID {task_id} nie istnieje.'}, status=404)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
            return JsonResponse({'error': 'Nieprawidłowy format danych JSON.'}, status=400)

        if 'completed' in data:
            task.completed = bool(data['completed'])

        if 'title' in data:
            title = data['title']
            if not isinstance(title, str) or not title.strip():
                return JsonResponse({'error': 'Treść zadania nie może być pusta.'}, status=400)
            task.title = title.strip()

        task.save()
        return JsonResponse(task.to_dict(), status=200)

    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Zadanie zostało pomyślnie usunięte.'}, status=200)

    return HttpResponseNotAllowed(['PATCH', 'DELETE'])
