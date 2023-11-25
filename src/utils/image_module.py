import os

def create_upload_dir(dir_name="images/"):
    os.makedirs(dir_name, exist_ok=True)
    
def save_uploded_images(images="images", dir_name="images/"):
    existing_files = len([f for f in os.listdir(dir_name) if f.startswith("image_")])
    
    for i, image in enumerate(images, 1):
            _, file_extension = os.path.splitext(image.filename)
            unique_filename = f"image_{existing_files + i}{file_extension}"
            
            print(unique_filename)
            
            with open(os.path.join(dir_name, unique_filename), "wb") as f:
                f.write(image.file.read())