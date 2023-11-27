from fastapi import APIRouter, UploadFile, File
from typing import List

from ..utils.image_module import *
from ..services.image_to_song import *

router = APIRouter()

@router.post("/upload")
async def get_songs_title(images: List[UploadFile] = File(...)):
    init_images_dir()
    try:
        save_uploded_images(images)
        get_recommend_songs()
        return {"message": f"{len(images)} images uploaded successfully"}
    except Exception as e:
        return {"error": f"Failed to upload images: {e}"}
