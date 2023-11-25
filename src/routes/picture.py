import os

from fastapi import APIRouter, UploadFile, File
from typing import List

from ulits import image_module

router = APIRouter()

@router.post("/upload")
async def upload_images(images: List[UploadFile] = File(...)):
    try:
        upload_folder = "images/"
        os.makedirs(upload_folder, exist_ok=True)

        existing_files = len([f for f in os.listdir(upload_folder) if f.startswith("image_")])

        for i, image in enumerate(images, 1):
            _, file_extension = os.path.splitext(image.filename)
            unique_filename = f"image_{existing_files + i}{file_extension}"
            
            with open(os.path.join(upload_folder, unique_filename), "wb") as f:
                f.write(image.file.read())

        return {"message": f"{len(images)} images uploaded successfully"}
    except Exception as e:
        return {"error": f"Failed to upload images: {e}"}
