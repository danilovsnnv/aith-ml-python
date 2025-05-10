from functools import lru_cache
from pydantic.v1 import BaseSettings, Field


class Settings(BaseSettings):
    cors_origins: list[str] = Field(default=['*'], env='CORS_ORIGINS')

    # RabbitMQ
    rabbitmq_user: str = Field(env='RABBITMQ_DEFAULT_USER')
    rabbitmq_pass: str = Field(env='RABBITMQ_DEFAULT_PASS')
    rabbitmq_exchange: str = Field(env='RABBITMQ_EXCHANGE')
    rabbitmq_queue: str = Field(env='RABBITMQ_QUEUE')
    rabbitmq_routing_key: str = Field(env='RABBITMQ_ROUTING_KEY')
    rabbitmq_host: str = Field(env='RABBITMQ_HOST', default='rabbitmq')
    rabbitmq_port: str = Field(env='RABBITMQ_PORT', default='5672')

    # Redis
    redis_host: str = Field(env='REDIS_HOST', default='redis')
    redis_port: str = Field(env='REDIS_PORT', default='6379')

    @property
    def rabbitmq_url(self) -> str:
        return f'amqp://{self.rabbitmq_user}:{self.rabbitmq_pass}@{self.rabbitmq_host}:{self.rabbitmq_port}/'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
