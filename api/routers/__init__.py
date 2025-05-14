from fastapi import FastAPI
from .prompt import router as prompt_router
from .model import router as info_router

base_url = "/api/v1"


def init_routers(app: FastAPI):
    app.include_router(prompt_router, prefix=base_url)
    app.include_router(info_router, prefix=base_url)
