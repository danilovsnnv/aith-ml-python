from __future__ import annotations

from functools import lru_cache
from pydantic.v1 import BaseSettings, Field

class Settings(BaseSettings):
    # crypto
    secret_key: str = Field(env='JWT_SECRET_KEY')
    algorithm: str = Field(default='HS256', env='ALGORITHM')
    access_token_expire_minutes: int = Field(default=30, env='ACCESS_TOKEN_EXPIRE_MINUTES')

    # cookie
    cookie_name: str = Field(default='access_token', env='COOKIE_NAME')
    cookie_max_age: int = Field(default=3600, env='COOKIE_MAX_AGE')

    # database
    database: str = Field(env='DATABASE_NAME')
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
