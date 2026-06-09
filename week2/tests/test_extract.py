if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "week2.tests"

import os
import pytest

from ..app.services.extract import extract_action_items


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_bullet_list_variants():
    text = """
    - [ ] write tests
    * fix API
    """.strip()

    items = extract_action_items(text)
    assert items == ["write tests", "fix API"]


def test_extract_keyword_prefixed_lines():
    text = """
    TODO: update README
    Action: call Bob
    This is context, not a task.
    """.strip()

    items = extract_action_items(text)
    assert items == ["TODO: update README", "Action: call Bob"]


@pytest.mark.parametrize("text", ["", "   ", "\n\t  \n"])
def test_extract_empty_or_whitespace_input(text):
    assert extract_action_items(text) == []


def _sample_text_for_llm() -> str:
    return """
    Product sync notes:

    The team reviewed the onboarding flow and agreed that the current empty state is
    confusing for new users. Alex will rewrite the first-run copy so it explains what
    happens after a note is saved. Priya should compare the latest API latency numbers
    with last week's baseline and report any regressions before Friday.

    Action: add a loading indicator while action items are being extracted.
    TODO: confirm whether the SQLite migration needs a rollback script.

    We also discussed several background topics, including pricing ideas and a possible
    redesign later in the semester. Those are not ready for immediate work. The meeting
    ended with one more next step: schedule a short QA session after the LLM endpoint is
    wired into the frontend.
    """.strip()


def test_extract_action_items_llm_runs_and_returns_action_items():
    from ..app.services.extract import extract_action_items_llm

    items = extract_action_items_llm(_sample_text_for_llm())

    assert isinstance(items, list)
    assert items
    assert all(isinstance(item, str) and item.strip() for item in items)
    assert len(items) == len({item.strip().lower() for item in items})


if __name__ == "__main__":
    from ..app.services.extract import extract_action_items_llm

    extracted_items = extract_action_items_llm(_sample_text_for_llm())
    print("extract_action_items_llm() output:")
    for index, item in enumerate(extracted_items, start=1):
        print(f"{index}. {item}")

    assert isinstance(extracted_items, list)
    assert extracted_items
    assert all(isinstance(item, str) and item.strip() for item in extracted_items)
