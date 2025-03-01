from typing import List
from fastapi import UploadFile

class ImagesService:

    def save_images(self, images: List[UploadFile]):
        for image in images:
            with open(f"app/images/{image.filename}", "wb") as f:
                f.write(image.file.read())
        return {"message": "Images saved successfully"}