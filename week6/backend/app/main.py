"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .db import apply_seed_if_needed, engine
from .models import Base
from .routers import action_items as action_items_router
from .routers import notes as notes_router
###
app = FastAPI(title="Modern Software Dev Starter (Week 7)", version="0.1.0")

# Ensure data dir exists
Path("data").mkdir(parents=True, exist_ok=True)

# Mount static frontend
#app.mount("/static", StaticFiles(directory="frontend"), name="static")
from pathlib import Path

base_dir = Path(__file__).parent.parent.parent
frontend_dir = base_dir / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compatibility with FastAPI lifespan events; keep on_event for simplicity here
@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    apply_seed_if_needed()


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("frontend/index.html")


# Routers
app.include_router(notes_router.router)
app.include_router(action_items_router.router)
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .db import apply_seed_if_needed, engine
from .models import Base
from .routers import action_items as action_items_router
from .routers import notes as notes_router

BASE_DIR = Path(__file__).parent.parent.parent

app = FastAPI(title="Modern Software Dev Starter (Week 7)", version="0.1.0")

(BASE_DIR / "data").mkdir(parents=True, exist_ok=True)

frontend_path = BASE_DIR / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
else:
    print(f"error: {frontend_path}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    apply_seed_if_needed()

@app.get("/")
async def root() -> FileResponse:
    index_path = BASE_DIR / "frontend" / "index.html"
    if not index_path.exists():
        raise RuntimeError(f"error: {index_path}")
    return FileResponse(str(index_path))


app.include_router(notes_router.router)
app.include_router(action_items_router.router)

