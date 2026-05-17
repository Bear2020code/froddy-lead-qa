from __future__ import annotations

import json
from pathlib import Path

from app.actions.mock_followup import generate_followup
from app.analysis.mock_detector import classify_dialogue, detect_loss_type
from app.ingest.csv_parser import Dialogue, parse_csv
from app.scoring.quality import calculate_quality_score


def mock_verdict(
    dialogue: Dialogue,
    classification: str,
    loss_type: str,
    draft: str,
    quality_score: dict,
) -> dict:
    draft_lower = draft.lower()
    seller_text = " ".join(m.text.lower() for m in dialogue.messages if m.side == "seller")

    if "+7" in draft_lower or "http://" in draft_lower or "https://" in draft_lower or "t.me/" in draft_lower or "wa.me/" in draft_lower:
        return {
            "verdict": "block",
            "reason": "Draft contains phone, external link or messenger link.",
        }

    if any(keyword in draft_lower for keyword in ["скидк", "дешевле", "20%"]):
        return {
            "verdict": "block",
            "reason": "Draft may promise discount or price concession without approval.",
        }

    if any(keyword in seller_text for keyword in ["скидк", "дешевле", "20%", "начать завтра"]):
        return {
            "verdict": "block",
            "reason": "Dialogue contains an unsafe seller promise: discount, price concession or unapproved deadline.",
        }

    if quality_score.get("has_conflict_markers") or classification == "conflict":
        return {
            "verdict": "hold",
            "reason": "Conflict context: automatic follow-up may worsen the situation.",
        }

    if classification == "negotiation":
        return {
            "verdict": "review",
            "reason": "Negotiation requires human review.",
        }

    if loss_type in {"soft_loss", "no_next_step"}:
        return {
            "verdict": "review",
            "reason": "Follow-up needs human check because context is incomplete.",
        }

    if loss_type in {"brutal_loss", "cold_trail"}:
        return {
            "verdict": "allow",
            "reason": "Standard soft follow-up is safe.",
        }

    return {
        "verdict": "review",
        "reason": "Fallback review.",
    }


def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    csv_path = project_root / "samples" / "avito_repair_demo_30_dialogues.csv"

    dialogues = parse_csv(csv_path)

    actions = []

    for dialogue in dialogues:
        quality = calculate_quality_score(dialogue)
        classification_result = classify_dialogue(dialogue, quality)
        classification = classification_result["classification"]
        loss_result = detect_loss_type(dialogue, classification, quality)
        loss_type = loss_result["loss_type"]

        followup = generate_followup(dialogue, loss_type, classification)

        if followup is None:
            continue

        verdict = mock_verdict(dialogue, classification, loss_type, followup["draft"], quality)

        actions.append(
            {
                "dialogue_id": dialogue.dialogue_id,
                "manager_name": dialogue.manager_name,
                "classification": classification,
                "loss_type": loss_type,
                "severity": loss_result["severity"],
                "evidence": loss_result["evidence"],
                "action_type": followup["action_type"],
                "draft": followup["draft"],
                "verdict": verdict["verdict"],
                "verdict_reason": verdict["reason"],
            }
        )

    print(f"Recommended actions: {len(actions)}")
    print(json.dumps(actions, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
