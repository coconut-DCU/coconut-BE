import os

from ..settings.path import *

def create_upload_dir(dir_name="images/"):
    os.makedirs(dir_name, exist_ok=True)  

def delete_image_files(dir_path = IMG_PATH):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
def init_images_dir():
    create_upload_dir()
    delete_image_files(IMG_PATH)

def save_uploded_images(images="images", dir_name="images/"):
    existing_files = len([f for f in os.listdir(dir_name) if f.startswith("image_")])
    
    for i, image in enumerate(images, 1):
            _, file_extension = os.path.splitext(image.filename)
            unique_filename = f"image_{existing_files + i}{file_extension}"
            
            with open(os.path.join(dir_name, unique_filename), "wb") as f:
                f.write(image.file.read())      