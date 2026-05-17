import json
from pathlib import Path

from app.pipeline import analyze_csv_file


def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    csv_path = project_root / "samples" / "avito_repair_demo_30_dialogues.csv"

    result = analyze_csv_file(csv_path)

    print(f"Recommended actions: {result['recommended_actions_count']}")
    print(json.dumps(result["recommended_actions"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
