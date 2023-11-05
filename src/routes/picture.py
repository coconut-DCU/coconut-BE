# 여러사진 받는 코드
from fastapi import APIRouter, UploadFile, File
import os
from typing import List

router = APIRouter()

@router.post("/upload")
async def upload_images(images: List[UploadFile]):
    try:
        upload_folder = "images/"
        os.makedirs(upload_folder, exist_ok=True)

        for image in images:
            with open(f"{upload_folder}{image.filename}", "wb") as f:
                f.write(image.file.read())

        return {"message": f"{len(images)} images uploaded successfully"}
    except Exception as e:
        return {"error": f"Failed to upload images: {e}"}
