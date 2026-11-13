document.addEventListener('DOMContentLoaded', () => {
    const btnFetch = document.getElementById('btn-fetch');
    const filterAvailable = document.getElementById('filter-available');
    const filterGenre = document.getElementById('filter-genre');
    const filterStatus = document.getElementById('filter-status');
    const filterPlatform = document.getElementById('filter-platform');
    const filterDeckSup = document.getElementById('filter-decksup');
    const filterSearch = document.getElementById('filter-search');
    const filterSort = document.getElementById('filter-sort');
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

        if (filterAvailable && filterAvailable.value !== '') {
            params.append('available', filterAvailable.value);
        }
        if (filterGenre && filterGenre.value !== '') {
            params.append('genre', filterGenre.value);
        }
        if (filterStatus && filterStatus.value !== '') {
            params.append('status', filterStatus.value);
        }
        if (filterPlatform && filterPlatform.value !== '') {
            params.append('platform', filterPlatform.value);
        }
        if (filterDeckSup && filterDeckSup.value !== '') {
            params.append('decksup', filterDeckSup.value);
        }
        const search = filterSearch ? filterSearch.value.trim() : '';
        if (search !== '') {
            params.append('search', search);
        }
        if (filterSort && filterSort.value !== '') {
            params.append('sort', filterSort.value);
        }

        const query = params.toString();
        return query ? `/api/gry/?${query}` : '/api/gry/';
    }

    function updatePreview() {
        if (apiUrlPreview) {
            apiUrlPreview.textContent = buildApiUrl();
        }
    }

    [filterAvailable, filterGenre, filterStatus, filterPlatform, filterDeckSup, filterSort].forEach(select => {
        if (select) {
            select.addEventListener('change', updatePreview);
        }
    });
    if (filterSearch) {
        filterSearch.addEventListener('input', updatePreview);
    }

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

            const total = typeof data.count === 'number' ? data.count : items.length;
            summaryCount.textContent = `Wyniki: ${items.length} z ${total}`;
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

    function createMetaItem(text) {
        const span = document.createElement('span');
        span.textContent = text;
        return span;
    }

    function createSeparator() {
        const span = document.createElement('span');
        span.classList.add('meta-separator');
        span.textContent = '|';
        return span;
    }

    function createStatusBadge(game) {
        const badge = document.createElement('span');
        badge.classList.add('game-status', `status-${game.status.toLowerCase()}`);
        badge.textContent = game.status_display || game.status;
        return badge;
    }

    function renderList(games) {
        gamesContainer.replaceChildren();

        games.forEach(game => {
            const item = document.createElement('div');
            item.classList.add('game-item');

            const header = document.createElement('div');
            header.classList.add('game-header');

            const title = document.createElement('h3');
            title.classList.add('game-title');
            title.textContent = game.title;

            const badgeGroup = document.createElement('div');
            badgeGroup.classList.add('badge-group');
            badgeGroup.appendChild(createStatusBadge(game));

            const availability = document.createElement('span');
            availability.classList.add('game-status');
            if (game.available) {
                availability.classList.add('status-available');
                availability.textContent = 'Dostępna';
            } else {
                availability.classList.add('status-unavailable');
                availability.textContent = 'Niedostępna';
            }
            badgeGroup.appendChild(availability);

            header.appendChild(title);
            header.appendChild(badgeGroup);

            const meta = document.createElement('div');
            meta.classList.add('game-meta');

            meta.appendChild(createMetaItem(`Gatunek: ${game.genre}`));
            meta.appendChild(createSeparator());
            meta.appendChild(createMetaItem(`Platforma: ${game.platform_display || game.platform}`));
            meta.appendChild(createSeparator());
            meta.appendChild(createMetaItem(`Rok: ${game.release_year}`));
            meta.appendChild(createSeparator());
            meta.appendChild(createMetaItem(`Ocena: ${game.rating}/10`));
            meta.appendChild(createSeparator());
            meta.appendChild(createMetaItem(`Cena: ${game.price} zł`));
            if (game.decksup) {
                meta.appendChild(createSeparator());
                meta.appendChild(createMetaItem(`SteamOS: Tak`));
            }

            const desc = document.createElement('p');
            desc.classList.add('game-description');
            desc.textContent = game.description;

            const footer = document.createElement('div');
            footer.classList.add('game-footer');

            const left = document.createElement('span');
            left.textContent = `ID: ${game.id}`;
            if (game.developer) {
                left.textContent += ` | Studio: ${game.developer}`;
            }

            const right = document.createElement('span');
            const dates = [];
            if (game.completion_date) {
                dates.push(`Ukończono: ${game.completion_date}`);
            }
            if (game.added_date) {
                dates.push(`Dodano: ${game.added_date}`);
            }
            right.textContent = dates.join(' | ');

            footer.appendChild(left);
            footer.appendChild(right);

            item.appendChild(header);
            item.appendChild(meta);
            item.appendChild(desc);
            item.appendChild(footer);

            gamesContainer.appendChild(item);
        });
    }

    if (btnFetch) {
        btnFetch.addEventListener('click', (e) => {
            e.preventDefault();
            loadGames();
        });
    }

    updatePreview();
    loadGames();
});
