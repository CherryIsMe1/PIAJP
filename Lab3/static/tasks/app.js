document.addEventListener('DOMContentLoaded', () => {
    let allTasks = [];
    let currentFilter = 'all';

    const taskForm = document.getElementById('task-form');
    const taskTitleInput = document.getElementById('task-title');
    const taskList = document.getElementById('task-list');
    const emptyState = document.getElementById('empty-state');
    const messageBox = document.getElementById('message-box');
    const totalCountEl = document.getElementById('total-count');
    const completedCountEl = document.getElementById('completed-count');
    const filterButtons = document.querySelectorAll('.filter-btn');

    let messageTimeout = null;

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

    function showMessage(text, isError = true) {
        if (!text) {
            messageBox.style.display = 'none';
            messageBox.textContent = '';
            return;
        }

        if (messageTimeout) {
            clearTimeout(messageTimeout);
        }

        messageBox.textContent = text;
        messageBox.className = 'message-box ' + (isError ? 'error' : 'success');
        messageBox.style.display = 'block';

        messageTimeout = setTimeout(() => {
            messageBox.style.display = 'none';
            messageBox.textContent = '';
        }, 4000);
    }

    function updateCounters() {
        const total = allTasks.length;
        const completed = allTasks.filter(task => task.completed).length;

        totalCountEl.textContent = total;
        completedCountEl.textContent = completed;
    }

    function getFilteredTasks(tasks) {
        if (currentFilter === 'active') {
            return tasks.filter(t => !t.completed);
        }
        if (currentFilter === 'completed') {
            return tasks.filter(t => t.completed);
        }
        return tasks;
    }

    function renderTasks(tasksToRender) {
        taskList.textContent = '';

        if (tasksToRender.length === 0) {
            emptyState.style.display = 'block';
        } else {
            emptyState.style.display = 'none';
        }

        tasksToRender.forEach(task => {
            const li = document.createElement('li');
            li.className = 'task-item' + (task.completed ? ' completed' : '');
            li.dataset.id = task.id;

            const contentWrapper = document.createElement('div');
            contentWrapper.className = 'task-content-wrapper';

            const toggleBtn = document.createElement('button');
            toggleBtn.type = 'button';
            toggleBtn.className = 'task-toggle-btn';
            toggleBtn.setAttribute('aria-label', task.completed ? 'Oznacz jako aktywne' : 'Oznacz jako ukończone');
            toggleBtn.textContent = task.completed ? '✓' : '';

            toggleBtn.addEventListener('click', () => {
                toggleTask(task.id, task.completed);
            });

            const titleSpan = document.createElement('span');
            titleSpan.className = 'task-title-text';
            titleSpan.textContent = task.title;

            contentWrapper.appendChild(toggleBtn);
            contentWrapper.appendChild(titleSpan);

            const actionsWrapper = document.createElement('div');
            actionsWrapper.className = 'task-actions';

            const deleteBtn = document.createElement('button');
            deleteBtn.type = 'button';
            deleteBtn.className = 'btn-delete';
            deleteBtn.setAttribute('aria-label', 'Usuń zadanie');
            deleteBtn.textContent = 'Usuń';

            deleteBtn.addEventListener('click', () => {
                deleteTask(task.id);
            });

            actionsWrapper.appendChild(deleteBtn);

            li.appendChild(contentWrapper);
            li.appendChild(actionsWrapper);

            taskList.appendChild(li);
        });
    }

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

    async function addTask(title) {
        const trimmedTitle = title.trim();

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

            allTasks.unshift(newTask);
            renderTasks(getFilteredTasks(allTasks));
            updateCounters();

            taskTitleInput.value = '';
            showMessage('Zadanie dodane pomyślnie!', false);
        } catch (error) {
            showMessage(error.message, true);
        }
    }

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

            allTasks = allTasks.filter(t => t.id !== id);
            renderTasks(getFilteredTasks(allTasks));
            updateCounters();

            showMessage('Zadanie zostało usunięte.', false);
        } catch (error) {
            showMessage(error.message, true);
        }
    }

    taskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        addTask(taskTitleInput.value);
    });

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderTasks(getFilteredTasks(allTasks));
        });
    });

    loadTasks();
});
