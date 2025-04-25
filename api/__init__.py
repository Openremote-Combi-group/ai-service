from fastapi import FastAPI
from api.routers import init_routers
from .cors import init_cors

app = FastAPI(
    title="OpenRemote AI service",
)


# Init modules
init_routers(app)
init_cors(app)