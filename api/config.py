from pydantic_settings import BaseSettings
from pydantic import HttpUrl


class Config(BaseSettings):
    debug: bool = False

    openai_api_key: str

    ollama_host: HttpUrl
    openremote_host: HttpUrl
    openremote_client_id: str
    openremote_client_secret: str

    cors_allowed_domains: set[str] = set()


config = Config()
