from fastapi import APIRouter
import ollama

router = APIRouter(
    prefix="/model",
    tags=["models"]
)


@router.get("/")
async def list_all_models() -> list[ollama.ListResponse.Model]:
    ollama_client = ollama.AsyncClient()

    models = await ollama_client.list()

    return models.models


@router.get("/")
async def list_all_models() -> list[ollama.ListResponse.Model]:
    ollama_client = ollama.AsyncClient()

    models = await ollama_client.list()

    return models.models