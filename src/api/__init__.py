from fastapi import APIRouter

from src.api import image

router = APIRouter()
router.include_router(image.router, prefix="/api", tags=["image"])

__all__ = ["router"]