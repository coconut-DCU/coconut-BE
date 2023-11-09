import uvicorn
from fastapi import FastAPI
from src.routes import picture
from fastapi.logger import logger

app = FastAPI()
#app.include_router(img.router, prefix="/api", tags=["picture"])
app.include_router(picture.router, prefix="/api", tags=["picture"])

if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")