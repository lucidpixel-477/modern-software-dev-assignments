def _create_action_item(client, description: str) -> dict:
    r = client.post("/action-items/", json={"description": description})
    assert r.status_code == 201, r.text
    return r.json()


# ── Task 4: action items tests ─────────────────────────────────────


def test_create_and_complete_action_item(client):
    item = _create_action_item(client, "Ship it")
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_list_action_items_with_completed_filter(client):
    open_item = _create_action_item(client, "Open task")
    done_item = _create_action_item(client, "Done task")
    client.put(f"/action-items/{done_item['id']}/complete")

    r = client.get("/action-items/", params={"completed": "true"})
    assert r.status_code == 200
    completed_data = r.json()
    assert completed_data["total"] == 1
    assert {item["id"] for item in completed_data["items"]} == {done_item["id"]}
    assert all(item["completed"] is True for item in completed_data["items"])

    r = client.get("/action-items/", params={"completed": "false"})
    assert r.status_code == 200
    open_data = r.json()
    assert open_data["total"] == 1
    assert {item["id"] for item in open_data["items"]} == {open_item["id"]}
    assert all(item["completed"] is False for item in open_data["items"])


def test_bulk_complete_marks_all_requested_items(client):
    first = _create_action_item(client, "Task 1")
    second = _create_action_item(client, "Task 2")
    third = _create_action_item(client, "Task 3")

    r = client.post("/action-items/bulk-complete", json={"ids": [first["id"], third["id"]]})
    assert r.status_code == 200, r.text
    updated = r.json()
    assert [item["id"] for item in updated] == [first["id"], third["id"]]
    assert all(item["completed"] is True for item in updated)

    r = client.get("/action-items/", params={"completed": "true"})
    assert r.status_code == 200
    completed_ids = {item["id"] for item in r.json()["items"]}
    assert completed_ids == {first["id"], third["id"]}

    r = client.get("/action-items/", params={"completed": "false"})
    assert r.status_code == 200
    open_ids = {item["id"] for item in r.json()["items"]}
    assert open_ids == {second["id"]}


def test_bulk_complete_rolls_back_on_invalid_id(client):
    first = _create_action_item(client, "Task 1")
    second = _create_action_item(client, "Task 2")

    r = client.post("/action-items/bulk-complete", json={"ids": [first["id"], 999999]})
    assert r.status_code == 404

    r = client.get("/action-items/", params={"completed": "true"})
    assert r.status_code == 200
    assert r.json()["items"] == []

    r = client.get("/action-items/", params={"completed": "false"})
    assert r.status_code == 200
    remaining_ids = {item["id"] for item in r.json()["items"]}
    assert remaining_ids == {first["id"], second["id"]}


# ── Task 8: pagination boundary tests for GET /action-items ────────


def test_list_action_items_first_page(client):
    for i in range(3):
        _create_action_item(client, f"Task {i}")

    r = client.get("/action-items/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 3
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["items"]) == 2


def test_list_action_items_second_page(client):
    for i in range(3):
        _create_action_item(client, f"Task {i}")

    r = client.get("/action-items/", params={"page": 2, "page_size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 3
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert len(data["items"]) == 1


def test_list_action_items_empty_last_page(client):
    for i in range(2):
        _create_action_item(client, f"Task {i}")

    r = client.get("/action-items/", params={"page": 5, "page_size": 10})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert data["page"] == 5
    assert data["page_size"] == 10
    assert data["items"] == []


def test_list_action_items_invalid_page_zero(client):
    r = client.get("/action-items/", params={"page": 0})
    assert r.status_code == 422


def test_list_action_items_invalid_page_negative(client):
    r = client.get("/action-items/", params={"page": -1})
    assert r.status_code == 422


def test_list_action_items_too_large_page_size(client):
    for i in range(5):
        _create_action_item(client, f"Task {i}")

    r = client.get("/action-items/", params={"page": 1, "page_size": 100})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 5
    assert len(data["items"]) == 5


def test_list_action_items_pagination_combined_with_completed_filter(client):
    for i in range(4):
        item = _create_action_item(client, f"Task {i}")
        if i % 2 == 0:
            client.put(f"/action-items/{item['id']}/complete")

    r = client.get("/action-items/", params={"completed": "true", "page": 1, "page_size": 1})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert data["page_size"] == 1
    assert len(data["items"]) == 1
