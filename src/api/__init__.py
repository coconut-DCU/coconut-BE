from fastapi import APIRouter

from src.api import image

router = APIRouter()
router.include_router(image.router, tag=["image"])

__all__ = ["router"]