from __future__ import annotations

import re


EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

URL_RE = re.compile(
    r"\b(?:https?://|www\.)[^\s<>()]+",
    re.IGNORECASE,
)

PHONE_RE = re.compile(
    r"(?<!\d)(?:\+7|8|7)?[\s\-()]*(?:\d[\s\-()]*){10}(?!\d)"
)

RU_PLATE_RE = re.compile(
    r"\b[АВЕКМНОРСТУХABEKMHOPCTYX]\s?\d{3}\s?[АВЕКМНОРСТУХABEKMHOPCTYX]{2}\s?\d{2,3}\b",
    re.IGNORECASE,
)


def mask_pii(value: object) -> str:
    text = "" if value is None else str(value)

    text = EMAIL_RE.sub("[EMAIL]", text)
    text = URL_RE.sub("[URL]", text)
    text = PHONE_RE.sub("[PHONE]", text)
    text = RU_PLATE_RE.sub("[CAR_PLATE]", text)

    return text
