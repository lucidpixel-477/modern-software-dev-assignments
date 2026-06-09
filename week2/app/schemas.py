from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class NoteCreateRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    content: Any = ""


class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str


class ActionItemsExtractRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    text: Any = ""
    save_note: Any = False


class ExtractedActionItemResponse(BaseModel):
    id: int
    text: str


class ActionItemsExtractResponse(BaseModel):
    note_id: int | None
    items: list[ExtractedActionItemResponse]


class ActionItemResponse(BaseModel):
    id: int
    note_id: int | None
    text: str
    done: bool
    created_at: str


class MarkActionItemDoneRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    done: Any = True


class MarkActionItemDoneResponse(BaseModel):
    id: int
    done: bool
