from fastapi import APIRouter, UploadFile
import os

router = APIRouter()

UPLOAD_DIR = "app/images"  # 이미지 저장 디렉토리 경로

@router.post("/upload")
async def upload_file(file: UploadFile):
    try:
        if file.content_type.startswith('image/'):
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as f:
                f.write(file.file.read())
            return {"message": "Image uploaded successfully", "file_path": file_path}
        else:
            return {"error": "Invalid file type. Only image files are allowed."}
    except Exception as e:
        return {"error": f"Failed to upload image. Error: {str(e)}"}


# routes 변수 추가
routes = router.routes
