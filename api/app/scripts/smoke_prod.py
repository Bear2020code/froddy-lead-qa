from __future__ import annotations

import json
import sys
import urllib.request
from urllib.error import HTTPError, URLError


DEFAULT_BASE_URL = "https://froddy-lead-qa-froddy.amvera.io"


def request_json(url: str, method: str = "GET", payload: dict | None = None) -> dict:
    data = None
    headers = {}

    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"

    request = urllib.request.Request(
        url=url,
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8")
            return json.loads(body)
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed: HTTP {error.code}: {body}") from error
    except URLError as error:
        raise RuntimeError(f"{method} {url} failed: {error}") from error


def main() -> None:
    base_url = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else DEFAULT_BASE_URL

    print(f"Smoke testing: {base_url}")

    health = request_json(f"{base_url}/health")
    assert health["status"] == "ok"
    print("OK /health")

    demo = request_json(f"{base_url}/v1/analyze-demo")
    assert demo["total_dialogues"] == 10
    assert demo["recommended_actions_count"] == 7

    verdicts = {
        item["dialogue_id"]: item["verdict"]
        for item in demo["recommended_actions"]
    }

    assert verdicts["d_006"] == "hold"
    assert verdicts["d_010"] == "block"
    print("OK /v1/analyze-demo")

    request_json(f"{base_url}/v1/decision-journal", method="DELETE")
    empty_journal = request_json(f"{base_url}/v1/decision-journal")
    assert empty_journal["items"] == []
    print("OK DELETE /v1/decision-journal")

    payload = {
        "dialogue_id": "d_006",
        "manager_name": "Игорь",
        "original_verdict": "hold",
        "human_decision": "hold",
        "action_type": "escalate",
        "verdict_rule_id": "conflict_requires_hold",
    }

    saved = request_json(
        f"{base_url}/v1/decision-journal",
        method="POST",
        payload=payload,
    )

    assert saved["item"]["dialogue_id"] == "d_006"
    assert saved["item"]["human_decision"] == "hold"
    print("OK POST /v1/decision-journal")

    journal = request_json(f"{base_url}/v1/decision-journal")
    assert len(journal["items"]) == 1
    assert journal["items"][0]["dialogue_id"] == "d_006"
    print("OK GET /v1/decision-journal")

    print("Smoke test passed")


if __name__ == "__main__":
    main()
