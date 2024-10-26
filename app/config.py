import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

app: FastAPI = FastAPI(
    version="1.0",
    title="Bowling Shoes Rental Service with LLM Integration and Prompt Engineering API",
    description="API for Bowling Shoes Rental Service with LLM Integration and Prompt Engineering",
    docs_url="/api/v1/docs",
    redoc_url=None,
)


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

    SUPABASE_PROJECT_URL: str = os.getenv("SUPABASE_PROJECT_URL", "")
    SUPABASE_API_KEY: str = os.getenv("SUPABASE_API_KEY", "")
    SUPABASE_DB_PASSWORD: str = os.getenv("SUPABASE_DB_PASSWORD", "")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GPT_MODEL: str = os.getenv("OPENAI_GPT_MODEL", "")

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
