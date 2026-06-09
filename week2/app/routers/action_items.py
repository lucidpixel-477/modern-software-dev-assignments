from __future__ import annotations

from fastapi import APIRouter

from .. import db
from ..errors import text_required
from ..schemas import (
    ActionItemResponse,
    ActionItemsExtractRequest,
    ActionItemsExtractResponse,
    MarkActionItemDoneRequest,
    MarkActionItemDoneResponse,
)
from ..services.extract import extract_action_items, extract_action_items_llm

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ActionItemsExtractResponse)
def extract(payload: ActionItemsExtractRequest) -> dict[str, object]:
    return _extract_with_strategy(payload, use_llm=False)


@router.post("/extract-llm", response_model=ActionItemsExtractResponse)
def extract_llm(payload: ActionItemsExtractRequest) -> dict[str, object]:
    return _extract_with_strategy(payload, use_llm=True)


def _extract_with_strategy(
    payload: ActionItemsExtractRequest,
    *,
    use_llm: bool,
) -> dict[str, object]:
    text = str(payload.text).strip()
    if not text:
        raise text_required()

    note_id: int | None = None
    if payload.save_note:
        note_id = db.insert_note(text)

    items = extract_action_items_llm(text) if use_llm else extract_action_items(text)
    ids = db.insert_action_items(items, note_id=note_id)
    return {"note_id": note_id, "items": [{"id": i, "text": t} for i, t in zip(ids, items)]}


@router.get("", response_model=list[ActionItemResponse])
def list_all(note_id: int | None = None) -> list[dict[str, object]]:
    rows = db.list_action_items(note_id=note_id)
    return [db.action_item_to_dict(row) for row in rows]


@router.post("/{action_item_id}/done", response_model=MarkActionItemDoneResponse)
def mark_done(action_item_id: int, payload: MarkActionItemDoneRequest) -> dict[str, object]:
    done = bool(payload.done)
    db.mark_action_item_done(action_item_id, done)
    return {"id": action_item_id, "done": done}


