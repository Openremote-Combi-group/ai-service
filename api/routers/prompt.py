from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from api.service import AiService

router = APIRouter(prefix="/prompt", tags=["Prompt"])

ai_service = AiService()


class PromptRequest(BaseModel):
    prompt: str
    context: list[Literal['asset', 'asset_type']]
    model: str = "gemma3:4b"
    temperature: float = 0.2


@router.post("/create")
def generate_rules(prompt_data: PromptRequest):
    return ai_service.generate_json_llm_chain(
        prompt_data.prompt,
        prompt_data.model,
        prompt_data.temperature
    )
