from fastapi import APIRouter, UploadFile, File
from typing import List
import os
import uuid

router = APIRouter()

@router.post("/api/upload1")
async def upload_images(images: List[UploadFile] = File(...)):
    try:
        upload_folder = "images/"
        os.makedirs(upload_folder, exist_ok=True)

        for image in images:
            # 클라이언트에서 사용한 파일 이름을 서버에서도 동일하게 사용
            file_name, file_extension = os.path.splitext(image.filename)
            unique_filename = f"{file_name}_{str(uuid.uuid4())}{file_extension}"
            
            with open(f"{upload_folder}{unique_filename}", "wb") as f:
                f.write(image.file.read())

        return {"message": f"{len(images)} images uploaded successfully"}
    except Exception as e:
        return {"error": f"Failed to upload images: {e}"}
