from typing import Annotated

from fastapi import APIRouter, Query
import ollama

from api.schemas import Model

router = APIRouter(
    prefix="/model",
    tags=["models"]
)

models = [
    Model(
        name="llama3.2:3b",
        provider="Ollama"
    )
]


@router.get("/")
async def list_all_models(
    provider: Annotated[str | None, Query(description='Filter models based on provider')]
) -> list[Model]:
    # ollama_client = ollama.AsyncClient()
    #
    # models = await ollama_client.list()

    return models
