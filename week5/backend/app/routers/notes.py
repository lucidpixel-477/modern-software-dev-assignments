from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NoteRead, NoteSearchResponse

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=NoteSearchResponse)
def list_notes(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
    db: Session = Depends(get_db),
) -> NoteSearchResponse:
    total = db.execute(select(func.count()).select_from(Note)).scalar_one()

    offset = (page - 1) * page_size
    rows = db.execute(
        select(Note).order_by(Note.id.desc()).offset(offset).limit(page_size)
    ).scalars().all()

    return NoteSearchResponse(
        items=[NoteRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/search", response_model=NoteSearchResponse)
def search_notes(
    q: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
    sort: Literal["created_desc", "title_asc"] = Query(default="created_desc"),
    db: Session = Depends(get_db),
) -> NoteSearchResponse:
    filters = []
    if q is not None and q.strip():
        search_term = f"%{q.strip()}%"
        filters.append(or_(Note.title.ilike(search_term), Note.content.ilike(search_term)))

    total_query = select(func.count()).select_from(Note)
    if filters:
        total_query = total_query.where(*filters)
    total = db.execute(total_query).scalar_one()

    query = select(Note)
    if filters:
        query = query.where(*filters)

    if sort == "title_asc":
        query = query.order_by(Note.title.asc(), Note.id.asc())
    else:
        query = query.order_by(Note.id.desc())

    offset = (page - 1) * page_size
    rows = db.execute(query.offset(offset).limit(page_size)).scalars().all()

    return NoteSearchResponse(
        items=[NoteRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)
