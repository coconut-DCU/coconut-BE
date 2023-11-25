from fastapi import FastAPI

from src import api
from src.settings.config import AppConfig

config = AppConfig()
app = FastAPI()

app.include_router(api.router)