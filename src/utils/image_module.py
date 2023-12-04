import os

from ..settings.path import *

def create_upload_directory(dir_name="images/"):
    os.makedirs(dir_name, exist_ok=True)  

def delete_files_in_directory(dir_path = IMG_PATH):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
def initialize_upload_directory():
    create_upload_directory()
    delete_files_in_directory(IMG_PATH)

def save_images_to_directory(images="images", dir_name="images/"):
    existing_files = len([f for f in os.listdir(dir_name) if f.startswith("image_")])
    
    for i, image in enumerate(images, 1):
            _, file_extension = os.path.splitext(image.filename)
            unique_filename = f"image_{existing_files + i}{file_extension}"
            
            with open(os.path.join(dir_name, unique_filename), "wb") as f:
                f.write(image.file.read())
                
def to_list():
    img_list = os.listdir(IMG_PATH)
    full_img_list = [IMG_PATH + "/" + image for image in img_list]
    return full_img_list