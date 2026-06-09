def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_delete_note(client):
    """DELETE /notes/{id} removes the note and returns 204; missing id returns 404."""
    # Create a note to delete
    r = client.post("/notes/", json={"title": "Delete me", "content": "To be removed"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    # Delete it
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    # Verify it is gone
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404

    # Deleting a non-existent note returns 404
    r = client.delete("/notes/99999")
    assert r.status_code == 404


def test_update_note(client):
    """PUT /notes/{id} updates title and content; missing id returns 404."""
    # Create a note to update
    r = client.post("/notes/", json={"title": "Old", "content": "Old content"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    # Update it
    r = client.put(f"/notes/{note_id}", json={"title": "New", "content": "New content"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "New"
    assert data["content"] == "New content"
    assert data["id"] == note_id

    # Verify the update persisted
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "New"

    # Updating a non-existent note returns 404
    r = client.put("/notes/99999", json={"title": "X", "content": "Y"})
    assert r.status_code == 404


def test_notes_validation(client):
    """POST /notes/ rejects empty or whitespace-only fields with 422."""
    cases = [
        ({"title": "", "content": "ok"}, "empty title"),
        ({"title": "   ", "content": "ok"}, "whitespace title"),
        ({"title": "ok", "content": ""}, "empty content"),
        ({"title": "ok", "content": "   "}, "whitespace content"),
        ({"title": "ok"}, "missing content"),
        ({"content": "ok"}, "missing title"),
    ]
    for payload, desc in cases:
        r = client.post("/notes/", json=payload)
        assert r.status_code == 422, f"{desc}: expected 422, got {r.status_code}"
