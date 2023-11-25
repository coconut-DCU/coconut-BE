import uvicorn

from fastapi import FastAPI

from src import api
from src.settings.config import AppConfig

config = AppConfig()
app = FastAPI()

app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)