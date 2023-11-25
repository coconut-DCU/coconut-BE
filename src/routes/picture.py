from fastapi import APIRouter, UploadFile, File
from typing import List

from ..utils.image_module import *

router = APIRouter()

@router.post("/upload")
async def upload_images(images: List[UploadFile] = File(...)):
    create_upload_dir()
    try:
        save_uploded_images(images)
        return {"message": f"{len(images)} images uploaded successfully"}
    except Exception as e:
        return {"error": f"Failed to upload images: {e}"}
