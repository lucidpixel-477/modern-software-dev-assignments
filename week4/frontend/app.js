function showError(msg) {
  const banner = document.getElementById('error-banner');
  banner.textContent = msg;
  banner.style.display = 'block';
  clearTimeout(banner._hideTimeout);
  banner._hideTimeout = setTimeout(() => { banner.style.display = 'none'; }, 5000);
}

async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) {
    let msg = await res.text();
    try {
      const parsed = JSON.parse(msg);
      if (parsed.detail) {
        if (Array.isArray(parsed.detail)) {
          msg = parsed.detail.map((d) => d.msg).join(', ');
        } else {
          msg = parsed.detail;
        }
      }
    } catch {
      // not JSON, use raw text
    }
    showError(msg);
    throw new Error(msg);
  }
  if (res.status === 204) return null;
  return res.json();
}

let editingNoteId = null;
let lastNotes = [];

function renderNotes(notes) {
  lastNotes = notes;
  const list = document.getElementById('notes');
  list.innerHTML = '';
  if (notes.length === 0) {
    const li = document.createElement('li');
    li.textContent = 'No notes found.';
    list.appendChild(li);
    return;
  }
  for (const n of notes) {
    const li = document.createElement('li');

    if (editingNoteId === n.id) {
      // Edit mode
      const titleInput = document.createElement('input');
      titleInput.value = n.title;
      titleInput.style.marginRight = '0.25rem';
      li.appendChild(titleInput);

      const contentInput = document.createElement('input');
      contentInput.value = n.content;
      contentInput.style.marginRight = '0.25rem';
      li.appendChild(contentInput);

      const saveBtn = document.createElement('button');
      saveBtn.textContent = 'Save';
      saveBtn.onclick = async () => {
        editingNoteId = null;
        await fetchJSON(`/notes/${n.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: titleInput.value, content: contentInput.value }),
        });
        refreshNotes();
      };
      li.appendChild(saveBtn);

      const cancelBtn = document.createElement('button');
      cancelBtn.textContent = 'Cancel';
      cancelBtn.onclick = () => {
        editingNoteId = null;
        refreshNotes();
      };
      li.appendChild(cancelBtn);
    } else {
      // Display mode
      const span = document.createElement('span');
      span.textContent = `${n.title}: ${n.content} `;
      li.appendChild(span);

      const editBtn = document.createElement('button');
      editBtn.textContent = 'Edit';
      editBtn.onclick = () => {
        editingNoteId = n.id;
        renderNotes(lastNotes);
      };
      li.appendChild(editBtn);

      const deleteBtn = document.createElement('button');
      deleteBtn.textContent = 'Delete';
      deleteBtn.onclick = async () => {
        editingNoteId = null;
        await fetchJSON(`/notes/${n.id}`, { method: 'DELETE' });
        refreshNotes();
      };
      li.appendChild(deleteBtn);
    }

    list.appendChild(li);
  }
}

async function loadNotes() {
  const notes = await fetchJSON('/notes/');
  renderNotes(notes);
}

function refreshNotes() {
  const q = document.getElementById('note-search').value.trim();
  if (q) {
    searchNotes();
  } else {
    loadNotes();
  }
}

let searchTimer = null;

function searchNotes() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(async () => {
    const q = document.getElementById('note-search').value.trim();
    const notes = await fetchJSON(`/notes/search/?q=${encodeURIComponent(q)}`);
    renderNotes(notes);
  }, 250);
}

async function loadActions() {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  const items = await fetchJSON('/action-items/');
  for (const a of items) {
    const li = document.createElement('li');
    const span = document.createElement('span');
    span.textContent = `${a.description} [${a.completed ? 'done' : 'open'}] `;
    li.appendChild(span);

    const toggleBtn = document.createElement('button');
    toggleBtn.textContent = a.completed ? 'Undo' : 'Complete';
    toggleBtn.onclick = async () => {
      await fetchJSON(`/action-items/${a.id}/toggle`, { method: 'PUT' });
      loadActions();
    };
    li.appendChild(toggleBtn);

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = async () => {
      await fetchJSON(`/action-items/${a.id}`, { method: 'DELETE' });
      loadActions();
    };
    li.appendChild(deleteBtn);

    list.appendChild(li);
  }
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
    document.getElementById('note-search').value = '';
    loadNotes();
  });

  document.getElementById('note-search').addEventListener('input', searchNotes);

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

  loadNotes();
  loadActions();
});
