from __future__ import annotations

import json
import re
from typing import Any

from ollama import chat

from ..config import settings

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> list[str]:
    lines = text.splitlines()
    extracted: list[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def extract_action_items_llm(text: str, model: str | None = None) -> list[str]:
    """Extract action items using an Ollama model with structured JSON output."""
    if not text.strip():
        return []

    selected_model = model or settings.ollama_action_items_model
    output_schema: dict[str, Any] = {
        "type": "array",
        "items": {"type": "string"},
    }

    schema_text = json.dumps(output_schema, ensure_ascii=False)
    response = chat(
        model=selected_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract action items from meeting notes and task lists. "
                    "Return only actionable tasks that someone should do next. "
                    "Do not include headings, background notes, or completed items."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Extract action items from the following text as a JSON array of "
                    f"strings matching this schema: {schema_text}\n\n{text}"
                ),
            },
        ],
        format=output_schema,
        options={"temperature": 0},
    )

    if isinstance(response, dict):
        message = response.get("message", {})
        content = message.get("content", "") if isinstance(message, dict) else ""
    else:
        content = response.message.content

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, list):
        return []

    seen: set[str] = set()
    items: list[str] = []
    for item in parsed:
        if not isinstance(item, str):
            continue
        cleaned = item.strip()
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        items.append(cleaned)
    return items
