from fastapi import FastAPI
from .config import config
from api.routers import init_routers
from .cors import init_cors
from .healthcheck import init_healthcheck

app = FastAPI(
    title="OpenRemote AI service"
)


# Init modules
init_routers(app)
init_cors(app)
init_healthcheck(app)