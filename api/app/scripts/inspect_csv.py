from __future__ import annotations

import json
from pathlib import Path

from app.ingest.csv_parser import parse_csv
from app.scoring.quality import calculate_quality_score


def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    csv_path = project_root / "samples" / "avito_repair_demo_30_dialogues.csv"

    dialogues = parse_csv(csv_path)

    print(f"Loaded dialogues: {len(dialogues)}")
    print()

    for dialogue in dialogues:
        score = calculate_quality_score(dialogue)
        print(f"{dialogue.dialogue_id} | {dialogue.ad_title} | manager={dialogue.manager_name}")
        print(json.dumps(score, ensure_ascii=False, indent=2))
        print("-" * 80)


if __name__ == "__main__":
    main()
