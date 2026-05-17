from __future__ import annotations

from app.ingest.csv_parser import Dialogue


def classify_dialogue(dialogue: Dialogue, quality_score: dict) -> dict:
    buyer_text = " ".join(m.text.lower() for m in dialogue.messages if m.side == "buyer")

    if any(marker in buyer_text for marker in ["работа онлайн", "без вложений", "пишите в телеграм"]):
        return {
            "classification": "spam",
            "confidence": 0.95,
            "rationale": "Message looks like spam, not a repair lead.",
        }

    if quality_score.get("has_conflict_markers"):
        return {
            "classification": "conflict",
            "confidence": 0.9,
            "rationale": "Buyer expressed irritation or complaint.",
        }

    if any(word in buyer_text for word in ["дешевле", "скидк", "другие предлагают"]):
        return {
            "classification": "negotiation",
            "confidence": 0.85,
            "rationale": "Buyer is negotiating price or terms.",
        }

    if quality_score.get("last_side") == "buyer":
        return {
            "classification": "lost",
            "confidence": 0.75,
            "rationale": "Buyer asked something and seller did not continue the dialogue.",
        }

    if quality_score.get("has_next_step") and quality_score.get("first_response_minutes") is not None:
        return {
            "classification": "hot_lead",
            "confidence": 0.8,
            "rationale": "Seller replied and proposed a next step.",
        }

    return {
        "classification": "warm_lead",
        "confidence": 0.6,
        "rationale": "Dialogue has some interest but no strong signal.",
    }


def detect_loss_type(dialogue: Dialogue, classification: str, quality_score: dict) -> dict:
    first_response = quality_score.get("first_response_minutes")
    last_side = quality_score.get("last_side")
    message_count = quality_score.get("message_count") or 0

    if classification in {"spam", "conflict", "negotiation"}:
        return {
            "loss_type": "no_loss",
            "severity": 0,
            "evidence": f"{classification} is handled by verdict logic, not as a standard lost lead.",
        }

    if first_response is None and last_side == "buyer":
        return {
            "loss_type": "brutal_loss",
            "severity": 4,
            "evidence": "Buyer sent a message, seller did not reply.",
        }

    if first_response is not None and first_response > 30:
        return {
            "loss_type": "brutal_loss",
            "severity": 4,
            "evidence": f"First response took {first_response} minutes.",
        }

    if quality_score.get("is_template_reply") and last_side == "buyer":
        return {
            "loss_type": "soft_loss",
            "severity": 3,
            "evidence": "Seller gave a short template-like reply and buyer asked a concrete follow-up.",
        }

    if not quality_score.get("has_next_step") and last_side == "seller":
        return {
            "loss_type": "no_next_step",
            "severity": 2,
            "evidence": "Seller ended the dialogue without a clear next step.",
        }

    # Good multi-message handled dialogues should not be flagged as cold trail in V0.1 mock logic.
    if (
        classification == "hot_lead"
        and last_side == "seller"
        and quality_score.get("has_next_step")
        and message_count >= 4
    ):
        return {
            "loss_type": "no_loss",
            "severity": 0,
            "evidence": "Dialogue has a clear next step and enough back-and-forth context.",
        }

    if last_side == "seller" and quality_score.get("has_next_step"):
        return {
            "loss_type": "cold_trail",
            "severity": 1,
            "evidence": "Seller proposed a next step, but buyer has not replied yet.",
        }

    return {
        "loss_type": "no_loss",
        "severity": 0,
        "evidence": "No clear loss pattern found.",
    }
