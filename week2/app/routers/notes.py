from __future__ import annotations

from fastapi import APIRouter

from .. import db
from ..errors import content_required, note_not_found
from ..schemas import NoteCreateRequest, NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse)
def create_note(payload: NoteCreateRequest) -> dict[str, object]:
    content = str(payload.content).strip()
    if not content:
        raise content_required()
    note_id = db.insert_note(content)
    note = db.get_note(note_id)
    return db.note_to_dict(note)


@router.get("", response_model=list[NoteResponse])
def list_all_notes() -> list[dict[str, object]]:
    rows = db.list_notes()
    return [db.note_to_dict(row) for row in rows]


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> dict[str, object]:
    row = db.get_note(note_id)
    if row is None:
        raise note_not_found()
    return db.note_to_dict(row)


