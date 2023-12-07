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
        song_urls = spotify.get_song_urls()
        
        return {"message": f"{len(images)} images uploaded successfully", "song_urls": song_urls}
    except Exception as e:
        return {"error": f"Failed to upload images: {e}"}
