from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Message:
    dialogue_id: str
    ad_title: str
    manager_name: str
    side: str
    text: str
    sent_at: datetime
    position: int


@dataclass(frozen=True)
class Dialogue:
    dialogue_id: str
    ad_title: str
    manager_name: str
    messages: list[Message]


REQUIRED_COLUMNS = {
    "dialogue_id",
    "ad_title",
    "manager_name",
    "side",
    "text",
    "sent_at",
}

VALID_SIDES = {"buyer", "seller"}


def parse_csv(path: str | Path) -> list[Dialogue]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"CSV missing required columns: {sorted(missing)}")

        grouped: dict[str, list[dict[str, str]]] = {}

        for row_number, row in enumerate(reader, start=2):
            dialogue_id = (row.get("dialogue_id") or "").strip()
            side = (row.get("side") or "").strip()

            if not dialogue_id:
                raise ValueError(f"Row {row_number}: dialogue_id is empty")

            if side not in VALID_SIDES:
                raise ValueError(
                    f"Row {row_number}: side must be one of {sorted(VALID_SIDES)}, got {side!r}"
                )

            try:
                datetime.fromisoformat((row.get("sent_at") or "").strip())
            except ValueError as exc:
                raise ValueError(f"Row {row_number}: invalid sent_at") from exc

            grouped.setdefault(dialogue_id, []).append(row)

    dialogues: list[Dialogue] = []

    for dialogue_id, rows in grouped.items():
        rows_sorted = sorted(rows, key=lambda item: datetime.fromisoformat(item["sent_at"].strip()))

        messages: list[Message] = []
        for position, row in enumerate(rows_sorted, start=1):
            messages.append(
                Message(
                    dialogue_id=dialogue_id,
                    ad_title=(row.get("ad_title") or "").strip(),
                    manager_name=(row.get("manager_name") or "").strip(),
                    side=(row.get("side") or "").strip(),
                    text=(row.get("text") or "").strip(),
                    sent_at=datetime.fromisoformat((row.get("sent_at") or "").strip()),
                    position=position,
                )
            )

        first_row = rows_sorted[0]
        dialogues.append(
            Dialogue(
                dialogue_id=dialogue_id,
                ad_title=(first_row.get("ad_title") or "").strip(),
                manager_name=(first_row.get("manager_name") or "").strip(),
                messages=messages,
            )
        )

    return sorted(dialogues, key=lambda dialogue: dialogue.dialogue_id)
