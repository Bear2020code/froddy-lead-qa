from __future__ import annotations

from datetime import datetime

from app.ingest.csv_parser import Dialogue


NEXT_STEP_KEYWORDS = [
    "замер",
    "созвон",
    "перезвон",
    "договор",
    "встрет",
    "приед",
    "напишите",
    "уточните",
    "запис",
    "смет",
    "рассчит",
]

CONFLICT_MARKERS = [
    "обман",
    "ужас",
    "верните",
    "никто не",
    "зачем тогда",
    "жалоб",
    "плохо",
    "недоволен",
    "сорвали",
]

TEMPLATE_MAX_LEN = 30


def calculate_quality_score(dialogue: Dialogue) -> dict:
    buyer_messages = [m for m in dialogue.messages if m.side == "buyer"]
    seller_messages = [m for m in dialogue.messages if m.side == "seller"]

    first_response_minutes = None

    if buyer_messages and seller_messages:
        first_buyer_at = buyer_messages[0].sent_at
        first_seller_after_buyer = next(
            (m for m in seller_messages if m.sent_at >= first_buyer_at),
            None,
        )
        if first_seller_after_buyer is not None:
            delta = first_seller_after_buyer.sent_at - first_buyer_at
            first_response_minutes = round(delta.total_seconds() / 60, 2)

    seller_text = "\n".join(m.text for m in seller_messages).lower()
    buyer_text = "\n".join(m.text for m in buyer_messages).lower()

    has_clarifying_question = any("?" in m.text for m in seller_messages)

    last_two_seller_text = " ".join(m.text.lower() for m in seller_messages[-2:])
    has_next_step = any(keyword in last_two_seller_text for keyword in NEXT_STEP_KEYWORDS)

    first_seller_text = seller_messages[0].text.strip() if seller_messages else ""
    is_template_reply = bool(first_seller_text) and len(first_seller_text) < TEMPLATE_MAX_LEN and "?" not in first_seller_text

    has_conflict_markers = any(marker in buyer_text for marker in CONFLICT_MARKERS)

    last_side = dialogue.messages[-1].side if dialogue.messages else None
    message_count = len(dialogue.messages)

    return {
        "first_response_minutes": first_response_minutes,
        "has_clarifying_question": has_clarifying_question,
        "has_next_step": has_next_step,
        "is_template_reply": is_template_reply,
        "has_conflict_markers": has_conflict_markers,
        "last_side": last_side,
        "message_count": message_count,
    }
