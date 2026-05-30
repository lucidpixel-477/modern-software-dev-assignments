def _create_note(client, title: str, content: str) -> None:
    r = client.post("/notes/", json={"title": title, "content": content})
    assert r.status_code == 201, r.text


def test_search_is_case_insensitive_and_returns_paginated_payload(client):
    _create_note(client, "Greeting", "Hello world")
    _create_note(client, "Unrelated", "Different body")
    _create_note(client, "Another", "says hello again")

    r = client.get("/notes/search", params={"q": "HELLO"})
    assert r.status_code == 200
    data = r.json()

    assert data["total"] == 2
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert [item["title"] for item in data["items"]] == ["Another", "Greeting"]


def test_search_supports_title_sort_and_pagination(client):
    _create_note(client, "bravo", "b")
    _create_note(client, "alpha", "a")
    _create_note(client, "charlie", "c")

    r = client.get(
        "/notes/search",
        params={"sort": "title_asc", "page": 1, "page_size": 2},
    )
    assert r.status_code == 200
    page_one = r.json()
    assert page_one["total"] == 3
    assert page_one["page"] == 1
    assert page_one["page_size"] == 2
    assert [item["title"] for item in page_one["items"]] == ["alpha", "bravo"]

    r = client.get(
        "/notes/search",
        params={"sort": "title_asc", "page": 2, "page_size": 2},
    )
    assert r.status_code == 200
    page_two = r.json()
    assert page_two["total"] == 3
    assert page_two["page"] == 2
    assert page_two["page_size"] == 2
    assert [item["title"] for item in page_two["items"]] == ["charlie"]


def test_search_blank_query_and_invalid_params(client):
    _create_note(client, "First", "alpha")
    _create_note(client, "Second", "beta")

    r = client.get("/notes/search", params={"q": "   ", "page_size": 1})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert data["page"] == 1
    assert data["page_size"] == 1
    assert len(data["items"]) == 1

    r = client.get("/notes/search", params={"sort": "bad_sort"})
    assert r.status_code == 422

    r = client.get("/notes/search", params={"page": 0})
    assert r.status_code == 422
