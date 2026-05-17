from __future__ import annotations

import hashlib
import sys
import time
import urllib.request
from pathlib import Path


DEFAULT_BASE_URL = "https://froddy-lead-qa-froddy.amvera.io"


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url=url,
        headers={
            "User-Agent": "froddy-lead-qa-deploy-check",
            "Cache-Control": "no-cache",
        },
        method="GET",
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> None:
    base_url = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else DEFAULT_BASE_URL
    cache_bust = int(time.time())

    project_root = Path(__file__).resolve().parents[3]
    local_path = project_root / "api" / "app" / "static" / "cabinet.html"

    local_html = local_path.read_text(encoding="utf-8")
    prod_html = fetch_text(f"{base_url}/cabinet?v={cache_bust}")

    local_hash = sha256_text(local_html)
    prod_hash = sha256_text(prod_html)

    print(f"Base URL: {base_url}")
    print(f"Local cabinet hash: {local_hash}")
    print(f"Prod cabinet hash:  {prod_hash}")
    print(f"Cabinet deployed:   {local_hash == prod_hash}")

    required_markers = [
        "Froddy Lead QA",
        "Clear journal",
        "Journal cleared",
        "Server: no decision yet",
        "Analyze your CSV",
        "PII masked before display/export",
    ]

    missing = [
        marker
        for marker in required_markers
        if marker not in prod_html
    ]

    if missing:
        print("Missing prod UI markers:")
        for marker in missing:
            print(f"- {marker}")
        raise SystemExit(1)

    print("Prod UI markers: OK")

    if local_hash != prod_hash:
        raise SystemExit("Prod cabinet differs from local cabinet.html")

    print("Prod UI deploy check passed")


if __name__ == "__main__":
    main()
