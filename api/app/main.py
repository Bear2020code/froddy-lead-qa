from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.pipeline import analyze_csv_file
from app.settings import settings

app = FastAPI(title="Froddy Lead QA API", version="0.1.0")


class AnalyzeCsvRequest(BaseModel):
    csv_text: str


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


@app.get("/v1/analyze-demo")
def analyze_demo() -> dict:
    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "samples" / "avito_repair_demo_30_dialogues.csv"

    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Demo CSV file not found.")

    return analyze_csv_file(csv_path)


@app.post("/v1/analyze-csv")
def analyze_csv(request: AnalyzeCsvRequest) -> dict:
    csv_text = request.csv_text.strip()

    if not csv_text:
        raise HTTPException(status_code=400, detail="csv_text is required.")

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        encoding="utf-8",
        delete=False,
    ) as temp_file:
        temp_file.write(csv_text)
        temp_path = Path(temp_file.name)

    try:
        return analyze_csv_file(temp_path)
    finally:
        temp_path.unlink(missing_ok=True)


@app.get("/cabinet", response_class=HTMLResponse)
def cabinet() -> str:
    cabinet_path = Path(__file__).resolve().parent / "static" / "cabinet.html"
    return cabinet_path.read_text(encoding="utf-8")
