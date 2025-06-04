from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import config


def init_cors(app: FastAPI):
    if config.debug:
        origins = [
            "http://localhost:8000",
            "http://localhost:9000",
            *config.cors_allowed_domains
        ]
    else:
        origins = [
            "http://localhost:9000",
            *config.cors_allowed_domains
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
