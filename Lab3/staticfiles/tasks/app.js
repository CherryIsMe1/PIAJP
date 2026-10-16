/**
 * TaskBoard - JavaScript Frontend dla Django REST API
 * Laboratorium 3: JavaScript w aplikacji Django
 */

document.addEventListener('DOMContentLoaded', () => {
    // Stan aplikacji w pamięci podręcznej frontendu
    let allTasks = [];
    let currentFilter = 'all'; // 'all' | 'active' | 'completed'

    // Elementy DOM
    const taskForm = document.getElementById('task-form');
    const taskTitleInput = document.getElementById('task-title');
    const taskList = document.getElementById('task-list');
    const emptyState = document.getElementById('empty-state');
    const messageBox = document.getElementById('message-box');
    const totalCountEl = document.getElementById('total-count');
    const completedCountEl = document.getElementById('completed-count');
    const filterButtons = document.querySelectorAll('.filter-btn');

    let messageTimeout = null;

    /**
     * Pobiera token CSRF z ciasteczek lub ukrytego pola formularza Django.
     */
    function getCsrfToken() {
        const cookie = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='));
        if (cookie) {
            return decodeURIComponent(cookie.split('=')[1]);
        }
        const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
        return tokenInput ? tokenInput.value : '';
    }

    /**
     * Wyświetla komunikat walidacji lub błędu API dla użytkownika.
     * @param {string} text - Treść komunikatu.
     * @param {boolean} isError - Czy komunikat jest błędem (true) czy informacją (false).
     */
    function showMessage(text, isError = true) {
        if (!text) {
            messageBox.style.display = 'none';
            messageBox.textContent = '';
            return;
        }

        if (messageTimeout) {
            clearTimeout(messageTimeout);
        }

        // Ważne: wstawianie treści przez textContent (ochrona przed XSS)
        messageBox.textContent = text;
        messageBox.className = 'message-box ' + (isError ? 'error' : 'success');
        messageBox.style.display = 'block';

        messageTimeout = setTimeout(() => {
            messageBox.style.display = 'none';
            messageBox.textContent = '';
        }, 4000);
    }

    /**
     * Aktualizuje liczniki zadań na podstawie tablicy allTasks.
     */
    function updateCounters() {
        const total = allTasks.length;
        const completed = allTasks.filter(task => task.completed).length;

        totalCountEl.textContent = total;
        completedCountEl.textContent = completed;
    }

    /**
     * Filtruje zadania według wybranego filtra ('all', 'active', 'completed').
     * @param {Array} tasks - Pełna lista zadań.
     * @returns {Array} Przefiltrowana lista zadań.
     */
    function getFilteredTasks(tasks) {
        if (currentFilter === 'active') {
            return tasks.filter(t => !t.completed);
        }
        if (currentFilter === 'completed') {
            return tasks.filter(t => t.completed);
        }
        return tasks;
    }

    /**
     * Renderuje listę zadań w drzewie DOM.
     * @param {Array} tasksToRender - Tablica zadań do wyświetlenia.
     */
    function renderTasks(tasksToRender) {
        taskList.textContent = ''; // czyszczenie poprzednich elementów listy

        if (tasksToRender.length === 0) {
            emptyState.style.display = 'block';
        } else {
            emptyState.style.display = 'none';
        }

        tasksToRender.forEach(task => {
            const li = document.createElement('li');
            li.className = 'task-item' + (task.completed ? ' completed' : '');
            li.dataset.id = task.id;

            // Kontener lewej strony (przycisk checkbox + tytuł)
            const contentWrapper = document.createElement('div');
            contentWrapper.className = 'task-content-wrapper';

            // Przycisk zmiany statusu
            const toggleBtn = document.createElement('button');
            toggleBtn.type = 'button';
            toggleBtn.className = 'task-toggle-btn';
            toggleBtn.setAttribute('aria-label', task.completed ? 'Oznacz jako aktywne' : 'Oznacz jako ukończone');
            toggleBtn.textContent = task.completed ? '✓' : '';

            // Obsługa kliknięcia zmiany statusu
            toggleBtn.addEventListener('click', () => {
                toggleTask(task.id, task.completed);
            });

            // Tytuł zadania - BEZWZGLĘDNIE textContent (wymóg bezpieczeństwa DOM)
            const titleSpan = document.createElement('span');
            titleSpan.className = 'task-title-text';
            titleSpan.textContent = task.title;

            contentWrapper.appendChild(toggleBtn);
            contentWrapper.appendChild(titleSpan);

            // Kontener prawej strony (przycisk usuwania)
            const actionsWrapper = document.createElement('div');
            actionsWrapper.className = 'task-actions';

            const deleteBtn = document.createElement('button');
            deleteBtn.type = 'button';
            deleteBtn.className = 'btn-delete';
            deleteBtn.setAttribute('aria-label', 'Usuń zadanie');
            deleteBtn.textContent = 'Usuń';

            // Obsługa usunięcia zadania
            deleteBtn.addEventListener('click', () => {
                deleteTask(task.id);
            });

            actionsWrapper.appendChild(deleteBtn);

            li.appendChild(contentWrapper);
            li.appendChild(actionsWrapper);

            taskList.appendChild(li);
        });
    }

    /**
     * Pobiera listę zadań z API backendu (wskazówka z slajdu 6).
     */
    async function loadTasks() {
        try {
            const response = await fetch('/api/tasks/');
            if (!response.ok) {
                throw new Error('Nie udało się pobrać zadań');
            }
            const tasks = await response.json();
            allTasks = tasks;
            renderTasks(getFilteredTasks(allTasks));
            updateCounters();
        } catch (error) {
            showMessage(error.message, true);
        }
    }

    /**
     * Dodaje nowe zadanie przez żądanie POST do API.
     * @param {string} title - Treść zadania.
     */
    async function addTask(title) {
        const trimmedTitle = title.trim();

        // Walidacja po stronie klienta (Wymóg jakościowy)
        if (!trimmedTitle) {
            showMessage('Treść zadania nie może być pusta!', true);
            taskTitleInput.focus();
            return;
        }

        try {
            const response = await fetch('/api/tasks/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ title: trimmedTitle })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || 'Błąd podczas dodawania zadania');
            }

            const newTask = await response.json();

            // Aktualizacja stanu i DOM bez przeładowywania strony
            allTasks.unshift(newTask);
            renderTasks(getFilteredTasks(allTasks));
            updateCounters();

            taskTitleInput.value = '';
            showMessage('Zadanie dodane pomyślnie!', false);
        } catch (error) {
            showMessage(error.message, true);
        }
    }

    /**
     * Zmienia status zadania (ukończone / aktywne) przez żądanie PATCH do API.
     * @param {number} id - ID zadania.
     * @param {boolean} currentStatus - Aktualny status ukończenia.
     */
    async function toggleTask(id, currentStatus) {
        const newStatus = !currentStatus;

        try {
            const response = await fetch(`/api/tasks/${id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ completed: newStatus })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || 'Nie udało się zaktualizować statusu zadania');
            }

            const updatedTask = await response.json();

            // Aktualizacja obiektu w tablicy lokalnej
            const taskIndex = allTasks.findIndex(t => t.id === id);
            if (taskIndex !== -1) {
                allTasks[taskIndex] = updatedTask;
            }

            renderTasks(getFilteredTasks(allTasks));
            updateCounters();
        } catch (error) {
            showMessage(error.message, true);
        }
    }

    /**
     * Usuwa zadanie przez żądanie DELETE do API.
     * @param {number} id - ID zadania.
     */
    async function deleteTask(id) {
        try {
            const response = await fetch(`/api/tasks/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                }
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || 'Nie udało się usunąć zadania');
            }

            // Usunięcie z tablicy lokalnej i odświeżenie DOM
            allTasks = allTasks.filter(t => t.id !== id);
            renderTasks(getFilteredTasks(allTasks));
            updateCounters();

            showMessage('Zadanie zostało usunięte.', false);
        } catch (error) {
            showMessage(error.message, true);
        }
    }

    // Obsługa wysłania formularza
    taskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        addTask(taskTitleInput.value);
    });

    // Obsługa przełączania filtrów
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderTasks(getFilteredTasks(allTasks));
        });
    });

    // Inicjalne pobranie listy zadań po załadowaniu strony
    loadTasks();
});
