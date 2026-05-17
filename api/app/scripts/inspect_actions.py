import json
from pathlib import Path

from app.actions.mock_followup import generate_followup
from app.analysis.mock_detector import classify_dialogue, detect_loss_type
from app.ingest.csv_parser import parse_csv
from app.scoring.quality import calculate_quality_score
from app.verdict import VerdictEngine


def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    csv_path = project_root / "samples" / "avito_repair_demo_30_dialogues.csv"

    dialogues = parse_csv(csv_path)
    verdict_engine = VerdictEngine()

    actions = []

    for dialogue in dialogues:
        quality = calculate_quality_score(dialogue)
        classification_result = classify_dialogue(dialogue, quality)
        classification = classification_result["classification"]
        loss_result = detect_loss_type(dialogue, classification, quality)

        if loss_result["loss_type"] == "no_loss" and classification not in {"conflict", "negotiation"}:
            continue

        followup = generate_followup(dialogue, loss_result["loss_type"], classification)

        if followup is None and classification == "conflict":
            followup = {
                "action_type": "escalate",
                "draft": "Передать диалог человеку: конфликтный контекст может ухудшиться от автоматического follow-up.",
            }

        if followup is None and classification == "negotiation":
            followup = {
                "action_type": "follow_up",
                "draft": "Передать человеку: покупатель торгуется, условия нельзя обещать без подтверждения.",
            }

        if followup is None:
            continue

        seller_text = " ".join(
            message.text for message in dialogue.messages if message.side == "seller"
        )

        action = {
            "dialogue_id": dialogue.dialogue_id,
            "manager_name": dialogue.manager_name,
            "classification": classification,
            "loss_type": loss_result["loss_type"],
            "severity": loss_result["severity"],
            "evidence": loss_result["evidence"],
            "seller_text": seller_text,
            "action_type": followup["action_type"],
            "draft": followup["draft"],
        }

        actions.append(verdict_engine.apply(action))

    print(f"Recommended actions: {len(actions)}")
    print(json.dumps(actions, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
