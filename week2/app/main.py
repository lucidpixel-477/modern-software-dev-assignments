from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .config import settings
from .db import init_db
from .routers import action_items, notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_title, lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return settings.index_html_path.read_text(encoding="utf-8")


app.include_router(notes.router)
app.include_router(action_items.router)


app.mount("/static", StaticFiles(directory=str(settings.frontend_dir)), name="static")
