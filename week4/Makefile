.PHONY: run test format lint seed

HOST ?= 127.0.0.1
PORT ?= 8000
PYTHON ?= python

run:
	$(PYTHON) -m uvicorn backend.app.main:app --reload --host $(HOST) --port $(PORT)

test:
	$(PYTHON) -m pytest -q backend/tests

format:
	$(PYTHON) -m black .
	$(PYTHON) -m ruff check . --fix

lint:
	$(PYTHON) -m ruff check .

seed:
	$(PYTHON) -c "from backend.app.db import apply_seed_if_needed; apply_seed_if_needed()"