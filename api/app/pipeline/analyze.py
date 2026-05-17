from __future__ import annotations

from pathlib import Path
from typing import Any

from app.actions.mock_followup import generate_followup
from app.analysis.mock_detector import classify_dialogue, detect_loss_type
from app.ingest.csv_parser import Dialogue, parse_csv
from app.scoring.quality import calculate_quality_score
from app.verdict import VerdictEngine


def analyze_csv_file(csv_path: str | Path) -> dict[str, Any]:
    dialogues = parse_csv(Path(csv_path))
    return analyze_dialogues(dialogues)


def analyze_dialogues(dialogues: list[Dialogue]) -> dict[str, Any]:
    verdict_engine = VerdictEngine()

    actions: list[dict[str, Any]] = []
    total_dialogues = len(dialogues)

    for dialogue in dialogues:
        quality = calculate_quality_score(dialogue)
        classification_result = classify_dialogue(dialogue, quality)
        classification = classification_result["classification"]
        loss_result = detect_loss_type(dialogue, classification, quality)

        if loss_result["loss_type"] == "no_loss" and classification not in {"conflict", "negotiation"}:
            continue

        followup = generate_followup(dialogue, loss_result["loss_type"], classification)

        if followup is None:
            continue

        seller_text = " ".join(
            message.text for message in dialogue.messages if message.side == "seller"
        )

        action = {
            "dialogue_id": dialogue.dialogue_id,
            "manager_name": dialogue.manager_name,
            "classification": classification,
            "classification_confidence": classification_result["confidence"],
            "classification_rationale": classification_result["rationale"],
            "loss_type": loss_result["loss_type"],
            "severity": loss_result["severity"],
            "evidence": loss_result["evidence"],
            "quality_score": quality,
            "seller_text": seller_text,
            "action_type": followup["action_type"],
            "draft": followup["draft"],
            "intent": followup.get("intent"),
            "tone": followup.get("tone"),
        }

        actions.append(verdict_engine.apply(action))

    return {
        "total_dialogues": total_dialogues,
        "recommended_actions_count": len(actions),
        "recommended_actions": actions,
    }
