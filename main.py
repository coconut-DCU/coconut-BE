import uvicorn
from fastapi import FastAPI
from src.routes import picture

from src.settings.config import AppConfig

config = AppConfig()
app = FastAPI()

app.include_router(picture.router, prefix="/api", tags=["picture"])

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)