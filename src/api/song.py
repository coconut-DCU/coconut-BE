from fastapi import APIRouter, UploadFile, File
from typing import List

from ..utils.image_module import *
from ..services.image_to_song import *
from ..services import spotify

router = APIRouter()


@router.post("/upload")
async def get_songs_title(images: List[UploadFile] = File(...)):
    initialize_upload_directory()
    try:
        save_images_to_directory(images)
        
        # file = [image.filename for image in images]
        # print(file)
        spotify.test2()
        
        return {"message": f"{len(images)} images uploaded successfully"}
    except Exception as e:
        return {"error": f"Failed to upload images: {e}"}
