import os

def create_upload_forder(forder_name):
    os.makedirs(forder_name, exist_ok=True)