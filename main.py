import uvicorn
from fastapi import FastAPI
from src.routes.router import router

app = FastAPI()
app.include_router(router, prefix="/api", tags=["picture"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)