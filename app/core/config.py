from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import json

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    app_name: str = "AI Research Assistant Pro"
    groq_api_key: str
    tavily_api_key: str

    # Read as a raw string from env to avoid JSON decoding issues on complex types
    # Accepts either a JSON array or a comma-separated list
    cors_origins_raw: str = Field(default="", alias="CORS_ORIGINS")

    @property
    def cors_origins(self) -> List[str]:
        v = (self.cors_origins_raw or "").strip()
        if not v:
            return []
        # Try JSON array first
        if v.startswith("["):
            try:
                data = json.loads(v)
                return [str(x).strip() for x in data if str(x).strip()]
            except Exception:
                pass
        # Fallback: comma-separated
        return [o.strip() for o in v.split(",") if o.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
