from pydantic_settings import BaseSettings
from pydantic import HttpUrl


class Config(BaseSettings):
    debug: bool = False

    ollama_url: HttpUrl

    cors_allowed_domains: set[str] = set()


config = Config()
