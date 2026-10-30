// Skrypt obsługi żądań fetch() i aktualizacji DOM (Laboratorium B)

document.addEventListener('DOMContentLoaded', () => {
    const btnFetch = document.getElementById('btn-fetch');
    const filterAvailable = document.getElementById('filter-available');
    const filterGenre = document.getElementById('filter-genre');
    const filterSearch = document.getElementById('filter-search');
    const apiUrlPreview = document.getElementById('api-url-preview');

    const loadingSpinner = document.getElementById('loading-spinner');
    const errorBox = document.getElementById('error-box');
    const errorDetails = document.getElementById('error-details');
    const emptyBox = document.getElementById('empty-box');
    const summaryBar = document.getElementById('summary-bar');
    const summaryCount = document.getElementById('summary-count');
    const gamesContainer = document.getElementById('games-container');

    function buildApiUrl() {
        const params = new URLSearchParams();

        if (filterAvailable.value !== '') {
            params.append('available', filterAvailable.value);
        }
        if (filterGenre.value !== '') {
            params.append('genre', filterGenre.value);
        }
        const search = filterSearch.value.trim();
        if (search !== '') {
            params.append('search', search);
        }

        const query = params.toString();
        return query ? `/api/gry/?${query}` : '/api/gry/';
    }

    function updatePreview() {
        apiUrlPreview.textContent = buildApiUrl();
    }

    filterAvailable.addEventListener('change', updatePreview);
    filterGenre.addEventListener('change', updatePreview);
    filterSearch.addEventListener('input', updatePreview);

    async function loadGames() {
        const url = buildApiUrl();
        updatePreview();

        btnFetch.disabled = true;
        loadingSpinner.classList.remove('hidden');
        errorBox.classList.add('hidden');
        emptyBox.classList.add('hidden');
        summaryBar.classList.add('hidden');
        gamesContainer.replaceChildren();

        try {
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`Błąd HTTP ${response.status}`);
            }

            const data = await response.json();
            const items = data.items || [];

            if (items.length === 0) {
                emptyBox.classList.remove('hidden');
                return;
            }

            renderList(items);

            summaryCount.textContent = `Wyniki: ${items.length}`;
            summaryBar.classList.remove('hidden');

        } catch (err) {
            console.error('Błąd pobierania danych:', err);
            errorDetails.textContent = err.message || 'Nie udało się pobrać danych.';
            errorBox.classList.remove('hidden');
        } finally {
            loadingSpinner.classList.add('hidden');
            btnFetch.disabled = false;
        }
    }

    function renderList(games) {
        gamesContainer.replaceChildren();

        games.forEach(game => {
            const item = document.createElement('div');
            item.classList.add('game-item');

            // Nagłówek: tytuł i status
            const header = document.createElement('div');
            header.classList.add('game-header');

            const title = document.createElement('h3');
            title.classList.add('game-title');
            title.textContent = game.title;

            const status = document.createElement('span');
            status.classList.add('game-status');
            if (game.available) {
                status.classList.add('status-available');
                status.textContent = 'Dostępna';
            } else {
                status.classList.add('status-unavailable');
                status.textContent = 'Niedostępna';
            }

            header.appendChild(title);
            header.appendChild(status);

            // Metadane: gatunek, rok, ocena
            const meta = document.createElement('div');
            meta.classList.add('game-meta');

            const genreSpan = document.createElement('span');
            genreSpan.textContent = `Gatunek: ${game.genre}`;

            const sep1 = document.createElement('span');
            sep1.classList.add('meta-separator');
            sep1.textContent = '|';

            const yearSpan = document.createElement('span');
            yearSpan.textContent = `Rok: ${game.release_year}`;

            const sep2 = document.createElement('span');
            sep2.classList.add('meta-separator');
            sep2.textContent = '|';

            const ratingSpan = document.createElement('span');
            ratingSpan.textContent = `Ocena: ${game.rating}/10`;

            meta.appendChild(genreSpan);
            meta.appendChild(sep1);
            meta.appendChild(yearSpan);
            meta.appendChild(sep2);
            meta.appendChild(ratingSpan);

            // Opis
            const desc = document.createElement('p');
            desc.classList.add('game-description');
            desc.textContent = game.description;

            // Stopka
            const footer = document.createElement('div');
            footer.classList.add('game-footer');

            const idSpan = document.createElement('span');
            idSpan.textContent = `ID: ${game.id}`;

            const dateSpan = document.createElement('span');
            dateSpan.textContent = game.added_date ? `Dodano: ${game.added_date}` : '';

            footer.appendChild(idSpan);
            footer.appendChild(dateSpan);

            item.appendChild(header);
            item.appendChild(meta);
            item.appendChild(desc);
            item.appendChild(footer);

            gamesContainer.appendChild(item);
        });
    }

    btnFetch.addEventListener('click', (e) => {
        e.preventDefault();
        loadGames();
    });

    updatePreview();
    loadGames();
});
