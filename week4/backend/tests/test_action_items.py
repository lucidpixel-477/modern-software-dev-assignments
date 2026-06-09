def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1


def test_action_items_validation(client):
    """POST /action-items/ rejects empty or whitespace-only description with 422."""
    cases = [
        ({"description": ""}, "empty description"),
        ({"description": "   "}, "whitespace description"),
        ({}, "missing description"),
    ]
    for payload, desc in cases:
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 422, f"{desc}: expected 422, got {r.status_code}"


def test_complete_missing_action_item(client):
    """PUT /action-items/{id}/complete returns 404 for non-existent item."""
    r = client.put("/action-items/99999/complete")
    assert r.status_code == 404


def test_toggle_action_item(client):
    """PUT /action-items/{id}/toggle flips completed status."""
    # Create
    r = client.post("/action-items/", json={"description": "Toggle me"})
    assert r.status_code == 201
    item_id = r.json()["id"]
    assert r.json()["completed"] is False

    # Toggle to done
    r = client.put(f"/action-items/{item_id}/toggle")
    assert r.status_code == 200
    assert r.json()["completed"] is True

    # Toggle back to undone
    r = client.put(f"/action-items/{item_id}/toggle")
    assert r.status_code == 200
    assert r.json()["completed"] is False

    # Toggle non-existent returns 404
    r = client.put("/action-items/99999/toggle")
    assert r.status_code == 404


def test_delete_action_item(client):
    """DELETE /action-items/{id} removes the item and returns 204."""
    # Create
    r = client.post("/action-items/", json={"description": "Delete me"})
    assert r.status_code == 201
    item_id = r.json()["id"]

    # Delete
    r = client.delete(f"/action-items/{item_id}")
    assert r.status_code == 204

    # Verify gone
    r = client.get("/action-items/")
    items = r.json()
    assert all(i["id"] != item_id for i in items)

    # Delete non-existent returns 404
    r = client.delete("/action-items/99999")
    assert r.status_code == 404
