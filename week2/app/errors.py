from __future__ import annotations

from fastapi import HTTPException


def bad_request(detail: str) -> HTTPException:
    return HTTPException(status_code=400, detail=detail)


def not_found(detail: str) -> HTTPException:
    return HTTPException(status_code=404, detail=detail)


def content_required() -> HTTPException:
    return bad_request("content is required")


def text_required() -> HTTPException:
    return bad_request("text is required")


def note_not_found() -> HTTPException:
    return not_found("note not found")
