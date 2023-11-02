# 왜안되냐

from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

@router.post("/upload")
async def upload_image(image: UploadFile):
    try:
        # 이미지를 저장할 디렉토리 경로
        upload_folder = "images/"
        
        os.makedirs(upload_folder, exist_ok=True)

        # 이미지를 지정된 디렉토리에 저장
        with open(f"{upload_folder}{image.filename}", "wb") as f:
            f.write(image.file.read())

        return {"message": "Image uploaded successfully"}
    except Exception as e:
        return {"error": f"Failed to upload image: {e}"}