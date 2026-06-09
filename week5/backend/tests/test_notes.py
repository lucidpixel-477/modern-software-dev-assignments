def _create_note(client, title: str, content: str) -> None:
    r = client.post("/notes/", json={"title": title, "content": content})
    assert r.status_code == 201, r.text


# ── Task 2: notes search tests ────────────────────────────────────


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


# ── Task 8: pagination boundary tests for GET /notes ──────────────


def test_list_notes_first_page(client):
    for i in range(3):
        _create_note(client, f"Note{i}", f"content{i}")

    r = client.get("/notes/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 3
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["items"]) == 2


def test_list_notes_second_page(client):
    for i in range(3):
        _create_note(client, f"Note{i}", f"content{i}")

    r = client.get("/notes/", params={"page": 2, "page_size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 3
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert len(data["items"]) == 1


def test_list_notes_empty_last_page(client):
    for i in range(2):
        _create_note(client, f"Note{i}", f"content{i}")

    r = client.get("/notes/", params={"page": 5, "page_size": 10})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert data["page"] == 5
    assert data["page_size"] == 10
    assert data["items"] == []


def test_list_notes_invalid_page_zero(client):
    r = client.get("/notes/", params={"page": 0})
    assert r.status_code == 422


def test_list_notes_invalid_page_negative(client):
    r = client.get("/notes/", params={"page": -1})
    assert r.status_code == 422


def test_list_notes_too_large_page_size(client):
    for i in range(5):
        _create_note(client, f"Note{i}", f"content{i}")

    r = client.get("/notes/", params={"page": 1, "page_size": 100})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 5
    assert len(data["items"]) == 5


# ── Task 9: performance / index tests ─────────────────────────────

import pytest
from sqlalchemy import text


@pytest.fixture
def db_session(client):
    """Access the underlying SQLAlchemy session through the FastAPI dependency override."""
    from backend.app.db import get_db
    from backend.app.main import app

    gen = app.dependency_overrides.get(get_db)
    if gen is None:
        pytest.skip("No DB override configured")
    session = next(gen())
    try:
        yield session
    finally:
        session.close()


def test_large_dataset_search_and_sort_no_regression(client):
    """Seed 100 notes and verify search + sorting + pagination hold up."""
    for i in range(100):
        _create_note(
            client,
            f"Note-{i:03d}",
            f"Content for note number {i}",
        )

    # Full scan returns all 100
    r = client.get("/notes/search", params={"page_size": 200})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 100
    assert len(data["items"]) == 100

    # Title-asc sort returns items in lexical order (Note-000, Note-001, …)
    r = client.get("/notes/search", params={"sort": "title_asc", "page_size": 5})
    assert r.status_code == 200
    page = r.json()
    assert page["total"] == 100
    assert page["page"] == 1
    titles = [item["title"] for item in page["items"]]
    assert titles == ["Note-000", "Note-001", "Note-002", "Note-003", "Note-004"]

    # Search with a term that matches content
    r = client.get("/notes/search", params={"q": "number 42"})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Note-042"


def test_index_used_for_title_sort(db_session):
    """Verify SQLite uses the composite index (title, id) for title_asc sort."""
    plan = db_session.execute(
        text("EXPLAIN QUERY PLAN "
             "SELECT title, id FROM notes ORDER BY title ASC, id ASC")
    ).fetchall()
    plan_text = " ".join(str(row[-1]) for row in plan)

    # With the ix_notes_title_id composite index, SQLite should avoid
    # "USE TEMP B-TREE" (filesort) and instead scan the index directly.
    assert "USE TEMP B-TREE" not in plan_text, (
        f"Expected no filesort; got plan: {plan_text}"
    )
    # The plan should mention the covering index.
    assert "ix_notes_title_id" in plan_text or "COVERING INDEX" in plan_text, (
        f"Expected covering index usage; got plan: {plan_text}"
    )


def test_index_used_for_completed_filter(db_session):
    """Verify SQLite uses the completed index when filtering action items."""
    plan = db_session.execute(
        text("EXPLAIN QUERY PLAN "
             "SELECT id FROM action_items WHERE completed = 0")
    ).fetchall()
    plan_text = " ".join(str(row[-1]) for row in plan)

    # Should scan the index rather than the full table.
    assert "SCAN action_items" not in plan_text or "USING INDEX" in plan_text, (
        f"Expected index scan; got plan: {plan_text}"
    )
