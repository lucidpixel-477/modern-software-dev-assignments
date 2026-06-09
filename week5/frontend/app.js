async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

const notesState = {
  q: '',
  sort: 'created_desc',
  page: 1,
  pageSize: 10,
  total: 0,
};

function updateNotesToolbar() {
  const resultCount = document.getElementById('notes-result-count');
  const pageLabel = document.getElementById('notes-page-label');
  const prevBtn = document.getElementById('notes-prev');
  const nextBtn = document.getElementById('notes-next');

  const total = notesState.total;
  const totalPages = total === 0 ? 1 : Math.ceil(total / notesState.pageSize);
  const currentPage = Math.min(notesState.page, totalPages);

  if (total === 0) {
    resultCount.textContent = '0 results';
  } else {
    const start = (currentPage - 1) * notesState.pageSize + 1;
    const end = Math.min(currentPage * notesState.pageSize, total);
    resultCount.textContent = `Showing ${start}-${end} of ${total} results`;
  }

  pageLabel.textContent = `Page ${currentPage} of ${totalPages}`;
  prevBtn.disabled = currentPage <= 1;
  nextBtn.disabled = currentPage >= totalPages;
}

async function loadNotes() {
  const list = document.getElementById('notes');
  list.innerHTML = '';

  const params = new URLSearchParams({
    page: String(notesState.page),
    page_size: String(notesState.pageSize),
    sort: notesState.sort,
  });
  if (notesState.q.trim()) {
    params.set('q', notesState.q.trim());
  }

  const data = await fetchJSON(`/notes/search?${params.toString()}`);
  notesState.total = data.total;
  notesState.page = data.page;
  notesState.pageSize = data.page_size;

  for (const n of data.items) {
    const li = document.createElement('li');
    li.textContent = `${n.title}: ${n.content}`;
    list.appendChild(li);
  }

  updateNotesToolbar();
}

const actionsState = {
  filter: 'all',
  page: 1,
  pageSize: 10,
  total: 0,
  selectedIds: new Set(),
};

function updateActionsToolbar() {
  const resultCount = document.getElementById('actions-result-count');
  const pageLabel = document.getElementById('actions-page-label');
  const prevBtn = document.getElementById('actions-prev');
  const nextBtn = document.getElementById('actions-next');

  const total = actionsState.total;
  const totalPages = total === 0 ? 1 : Math.ceil(total / actionsState.pageSize);
  const currentPage = Math.min(actionsState.page, totalPages);

  if (total === 0) {
    resultCount.textContent = '0 results';
  } else {
    const start = (currentPage - 1) * actionsState.pageSize + 1;
    const end = Math.min(currentPage * actionsState.pageSize, total);
    resultCount.textContent = `Showing ${start}-${end} of ${total} results`;
  }

  pageLabel.textContent = `Page ${currentPage} of ${totalPages}`;
  prevBtn.disabled = currentPage <= 1;
  nextBtn.disabled = currentPage >= totalPages;
}

function updateActionToolbar() {
  const countEl = document.getElementById('action-selected-count');
  const bulkBtn = document.getElementById('actions-bulk-complete');
  if (countEl) {
    countEl.textContent = `${actionsState.selectedIds.size} selected`;
  }
  if (bulkBtn) {
    bulkBtn.disabled = actionsState.selectedIds.size === 0;
  }
}

async function loadActions() {
  const list = document.getElementById('actions');
  list.innerHTML = '';

  const params = new URLSearchParams({
    page: String(actionsState.page),
    page_size: String(actionsState.pageSize),
  });
  if (actionsState.filter === 'active') {
    params.set('completed', 'false');
  } else if (actionsState.filter === 'completed') {
    params.set('completed', 'true');
  }

  const data = await fetchJSON(`/action-items/?${params.toString()}`);
  actionsState.total = data.total;
  actionsState.page = data.page;
  actionsState.pageSize = data.page_size;

  for (const a of data.items) {
    const li = document.createElement('li');
    li.className = 'action-item';

    if (!a.completed) {
      const sel = document.createElement('label');
      sel.className = 'action-sel';
      sel.title = 'Select for bulk complete';
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.dataset.id = String(a.id);
      cb.checked = actionsState.selectedIds.has(a.id);
      cb.addEventListener('change', () => {
        if (cb.checked) {
          actionsState.selectedIds.add(a.id);
        } else {
          actionsState.selectedIds.delete(a.id);
        }
        updateActionToolbar();
      });
      sel.appendChild(cb);
      li.appendChild(sel);
    }

    const desc = document.createElement('span');
    desc.className = 'action-desc';
    desc.textContent = a.description;
    li.appendChild(desc);

    if (!a.completed) {
      const badge = document.createElement('span');
      badge.className = 'action-badge action-badge-open';
      badge.textContent = 'open';
      li.appendChild(badge);

      const btn = document.createElement('button');
      btn.textContent = 'Complete';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions();
      };
      li.appendChild(btn);
    } else {
      const badge = document.createElement('span');
      badge.className = 'action-badge action-badge-done';
      badge.textContent = 'done';
      li.appendChild(badge);
    }

    list.appendChild(li);
  }

  updateActionToolbar();
  updateActionsToolbar();
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    notesState.page = 1;
    loadNotes();
  });

  document.getElementById('note-sort-select').addEventListener('change', async (e) => {
    notesState.sort = e.target.value;
    notesState.page = 1;
    loadNotes();
  });

  document.getElementById('note-search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    notesState.q = document.getElementById('note-search-input').value;
    notesState.sort = document.getElementById('note-sort-select').value;
    notesState.page = 1;
    loadNotes();
  });

  document.getElementById('notes-prev').addEventListener('click', async () => {
    if (notesState.page > 1) {
      notesState.page -= 1;
      loadNotes();
    }
  });

  document.getElementById('notes-next').addEventListener('click', async () => {
    const totalPages = notesState.total === 0 ? 1 : Math.ceil(notesState.total / notesState.pageSize);
    if (notesState.page < totalPages) {
      notesState.page += 1;
      loadNotes();
    }
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    loadActions();
  });

  const filterContainer = document.querySelector('.action-filters');
  if (filterContainer) {
    filterContainer.addEventListener('click', (e) => {
      const btn = e.target.closest('button[data-action-filter]');
      if (!btn) return;
      filterContainer.querySelectorAll('button').forEach((b) => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      actionsState.filter = btn.dataset.actionFilter;
      actionsState.selectedIds.clear();
      actionsState.page = 1;
      loadActions();
    });
  }

  document.getElementById('actions-prev').addEventListener('click', async () => {
    if (actionsState.page > 1) {
      actionsState.page -= 1;
      loadActions();
    }
  });

  document.getElementById('actions-next').addEventListener('click', async () => {
    const totalPages = actionsState.total === 0 ? 1 : Math.ceil(actionsState.total / actionsState.pageSize);
    if (actionsState.page < totalPages) {
      actionsState.page += 1;
      loadActions();
    }
  });

  const bulkBtn = document.getElementById('actions-bulk-complete');
  if (bulkBtn) {
    bulkBtn.addEventListener('click', async () => {
      if (actionsState.selectedIds.size === 0) return;
      await fetchJSON('/action-items/bulk-complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ids: [...actionsState.selectedIds] }),
      });
      actionsState.selectedIds.clear();
      loadActions();
    });
  }

  loadNotes();
  loadActions();
});
