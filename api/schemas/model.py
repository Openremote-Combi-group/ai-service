from typing import Literal
from pydantic import BaseModel


class Model(BaseModel):
    name: str
    provider: Literal['ollama', 'openai']