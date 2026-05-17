from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn

ROOT = Path(__file__).resolve().parent
API_DIR = ROOT / "api"

sys.path.insert(0, str(API_DIR))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "80"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
