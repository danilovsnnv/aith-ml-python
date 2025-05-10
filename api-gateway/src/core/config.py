from __future__ import annotations

from functools import lru_cache
from pydantic.v1 import AnyHttpUrl, Field, BaseSettings


class Settings(BaseSettings):
    # CORS
    allowed_origins: list[str] = ['http://localhost:8000']

    # routing mapping
    # {prefix: service_url}
    service_urls: dict[str, AnyHttpUrl] = {
        'interact': 'http://interactions:8000',
        'rec': 'http://recommendations:8000',
        'auth': 'http://auth:8000',
        'user': 'http://auth:8000',
    }
    auth_prefix: str = '/auth'

    # security
    secret_key: str = Field(env='JWT_SECRET_KEY')
    algorithm: str = Field('HS256', env='ALGORITHM')
    cookie_name: str = Field(default='access_token', env='COOKIE_NAME')

    class Config:
        env_file = '.env'

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
