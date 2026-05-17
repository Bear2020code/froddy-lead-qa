from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Froddy Lead QA"
    environment: str = "local"


settings = Settings()
