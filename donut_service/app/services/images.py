from typing import List
from fastapi import UploadFile

class ImagesService:

    def save_images(self, images: List[UploadFile]):
        saved_img_id = []
        for image in images:
            with open(f"app/images/{image.filename}", "wb") as f:
                f.write(image.file.read())
            saved_img_id.append(image.filename)
        # return {"message": "Images saved successfully"}
        return saved_img_id