# API Documentation

Base URL: `http://localhost:8000`

OpenAPI spec available at `/openapi.json` and `/docs` (Swagger UI) when the server is running.

---

## Notes

All note endpoints are under the `/notes` prefix.

### Schemas

**NoteCreate** (request body for create/update)

```json
{
  "title": "string (required, non-empty)",
  "content": "string (required, non-empty)"
}
```

**NoteRead** (response)

```json
{
  "id": "integer",
  "title": "string",
  "content": "string"
}
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/notes/` | List all notes |
| `POST` | `/notes/` | Create a new note |
| `GET` | `/notes/search/?q={query}` | Search notes by title and content |
| `GET` | `/notes/{note_id}` | Get a single note by ID |
| `PUT` | `/notes/{note_id}` | Update a note |
| `DELETE` | `/notes/{note_id}` | Delete a note |

#### `GET /notes/`

Returns all notes ordered by ID.

- **Response**: `200` — `list[NoteRead]`

#### `POST /notes/`

Creates a new note. Both `title` and `content` are validated as non-empty (returns 422 if empty).

- **Request body**: `NoteCreate`
- **Response**: `201` — `NoteRead`
- **Errors**: `422` on validation failure (empty title or content)

#### `GET /notes/search/?q={query}`

Searches notes by matching `q` against both title and content using case-insensitive substring matching (SQLite `LIKE`). If `q` is omitted or empty, returns all notes.

- **Query params**: `q` (string, optional)
- **Response**: `200` — `list[NoteRead]`

#### `GET /notes/{note_id}`

Returns a single note by its ID.

- **Response**: `200` — `NoteRead`
- **Errors**: `404` if the note does not exist

#### `PUT /notes/{note_id}`

Replaces the title and content of an existing note.

- **Request body**: `NoteCreate`
- **Response**: `200` — `NoteRead`
- **Errors**: `404` if the note does not exist, `422` on validation failure

#### `DELETE /notes/{note_id}`

Deletes a note.

- **Response**: `204` (no content)
- **Errors**: `404` if the note does not exist

---

## Action Items

All action-item endpoints are under the `/action-items` prefix.

### Schemas

**ActionItemCreate** (request body)

```json
{
  "description": "string (required, non-empty)"
}
```

**ActionItemRead** (response)

```json
{
  "id": "integer",
  "description": "string",
  "completed": "boolean"
}
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/action-items/` | List all action items |
| `POST` | `/action-items/` | Create a new action item |
| `PUT` | `/action-items/{item_id}/complete` | Mark an item as completed |
| `PUT` | `/action-items/{item_id}/toggle` | Toggle completion status |
| `DELETE` | `/action-items/{item_id}` | Delete an action item |

#### `GET /action-items/`

Returns all action items ordered by ID.

- **Response**: `200` — `list[ActionItemRead]`

#### `POST /action-items/`

Creates a new action item. The `completed` field is always initialized to `false`. The description is validated as non-empty.

- **Request body**: `ActionItemCreate`
- **Response**: `201` — `ActionItemRead`
- **Errors**: `422` on validation failure (empty description)

#### `PUT /action-items/{item_id}/complete`

Sets the action item's `completed` field to `true`.

- **Response**: `200` — `ActionItemRead`
- **Errors**: `404` if the item does not exist

#### `PUT /action-items/{item_id}/toggle`

Flips the action item's `completed` field (`true` → `false`, `false` → `true`).

- **Response**: `200` — `ActionItemRead`
- **Errors**: `404` if the item does not exist

#### `DELETE /action-items/{item_id}`

Deletes an action item.

- **Response**: `204` (no content)
- **Errors**: `404` if the item does not exist

---

## Extraction Service (not exposed as an API endpoint)

The module `backend/app/services/extract.py` provides `extract_action_items(text: str) -> list[str]`, which parses a block of text and returns lines that look like action items:

- Lines ending with `!` (e.g. `"Ship feature!"`)
- Lines starting with `todo:` (case-insensitive, e.g. `"TODO: explore the app!"`)
- Leading `- ` bullet markers are stripped from extracted lines

This function is used internally (e.g. in tests) but is **not currently exposed** through any HTTP endpoint. Task 4 of `docs/TASKS.md` suggests optionally adding `POST /notes/{id}/extract` to convert note content into action items, but this has not been implemented.

---

## Other Routes

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves the frontend SPA (`frontend/index.html`) |
| `GET` | `/static/{path}` | Static files from `frontend/` (CSS, JS) |
| `GET` | `/openapi.json` | Auto-generated OpenAPI 3.0 spec |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc UI |

---

## Error Responses

All endpoints may return:

| Status | Meaning |
|--------|---------|
| `404` | Resource not found (invalid ID) |
| `422` | Validation error (empty required field, malformed body) |
| `500` | Internal server error |

Validation errors (422) include a `detail` field with an array of error objects, each containing `loc` (field location) and `msg` (error message).
