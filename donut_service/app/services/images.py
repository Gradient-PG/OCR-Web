from typing import List
from fastapi import UploadFile
from ..repository.mongodb.images import ImageRepository
from ..entity.image import ImageEntity

class ImagesService:

    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def save_images(self, input_images: List[UploadFile]):
        images = [
            ImageEntity(
                image_name=image.filename,
                image_data=image.file.read()
            )
            for image in input_images
        ]

        return self.image_repository.save_images(images)

    def get_all_images(self):
        return self.image_repository.get_all_images()
