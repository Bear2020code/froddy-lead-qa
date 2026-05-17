from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _journal_path() -> Path:
    project_root = Path(__file__).resolve().parents[3]
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "decision_journal.jsonl"


def append_decision(decision: dict[str, Any]) -> dict[str, Any]:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **decision,
    }

    path = _journal_path()

    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


def list_decisions(limit: int = 100) -> list[dict[str, Any]]:
    path = _journal_path()

    if not path.exists():
        return []

    records: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            records.append(json.loads(line))

    return list(reversed(records[-limit:]))


def clear_decisions() -> dict[str, bool]:
    path = _journal_path()

    if path.exists():
        path.unlink()

    return {"cleared": True}
