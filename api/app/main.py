from fastapi import FastAPI

from app.settings import settings

app = FastAPI(title="Froddy Lead QA API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }
