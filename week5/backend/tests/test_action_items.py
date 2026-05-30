def _create_action_item(client, description: str) -> dict:
    r = client.post("/action-items/", json={"description": description})
    assert r.status_code == 201, r.text
    return r.json()


def test_create_and_complete_action_item(client):
    item = _create_action_item(client, "Ship it")
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1


def test_list_action_items_with_completed_filter(client):
    open_item = _create_action_item(client, "Open task")
    done_item = _create_action_item(client, "Done task")
    client.put(f"/action-items/{done_item['id']}/complete")

    r = client.get("/action-items/", params={"completed": "true"})
    assert r.status_code == 200
    completed_items = r.json()
    assert {item["id"] for item in completed_items} == {done_item["id"]}
    assert all(item["completed"] is True for item in completed_items)

    r = client.get("/action-items/", params={"completed": "false"})
    assert r.status_code == 200
    open_items = r.json()
    assert {item["id"] for item in open_items} == {open_item["id"]}
    assert all(item["completed"] is False for item in open_items)


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
    completed_ids = {item["id"] for item in r.json()}
    assert completed_ids == {first["id"], third["id"]}

    r = client.get("/action-items/", params={"completed": "false"})
    assert r.status_code == 200
    open_ids = {item["id"] for item in r.json()}
    assert open_ids == {second["id"]}


def test_bulk_complete_rolls_back_on_invalid_id(client):
    first = _create_action_item(client, "Task 1")
    second = _create_action_item(client, "Task 2")

    r = client.post("/action-items/bulk-complete", json={"ids": [first["id"], 999999]})
    assert r.status_code == 404

    r = client.get("/action-items/", params={"completed": "true"})
    assert r.status_code == 200
    assert r.json() == []

    r = client.get("/action-items/", params={"completed": "false"})
    assert r.status_code == 200
    remaining_ids = {item["id"] for item in r.json()}
    assert remaining_ids == {first["id"], second["id"]}
