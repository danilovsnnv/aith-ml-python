from __future__ import annotations

from functools import lru_cache
from pydantic.v1 import BaseSettings, Field


class Settings(BaseSettings):
    database: str = Field(env='POSTGRES_DB')
    username: str = Field(env='POSTGRES_USER')
    password: str = Field(env='POSTGRES_PASSWORD')
    host: str = Field('localhost', env='DATABASE_HOST')
    port: int = Field(5432, env='DATABASE_PORT')
    query_params: dict[str, str] = Field(default_factory=dict)

    class Config:
        env_file = '.env'
        case_sensitive = True

@lru_cache
def get_setting() -> Settings:
    return Settings()

settings = get_setting()
