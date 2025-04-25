from fastapi import FastAPI
from .prompt import router as prompt_router

base_url = "/api/v1"


def init_routers(app: FastAPI):
    app.include_router(prompt_router, prefix=base_url)
