from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
from app.entity.image import ImageEntity
import os
import logging

class ImageRepository:
    def __init__(self, database_name="donut_service_database"):
        """
        Initialize the repository with a MongoDB connection.
        
        :param database_name: Name of the database to use.
        """
        self.client = MongoClient(
            host=os.getenv("MONGO_HOST", "mongodb"),
            port=int(os.getenv("MONGO_PORT", 27017)),
            username=os.getenv("MONGO_USER", "root"),
            password=os.getenv("MONGO_PASS", "pass"),
            )
        self.db = self.client[database_name]
        self.fs = gridfs.GridFS(self.db)  # GridFS for storing large files
        self.collection = self.db['images_metadata']  # Metadata collection

    def save_image(self, image: ImageEntity) -> str:
        """
        Save an image and its metadata to MongoDB.

        :param image: An ImageEntity object containing image data and metadata.
        :return: The ID of the saved image.
        """
        # Check if an image with the same name already exists
        existing_metadata = self.collection.find_one({"image_name": image.image_name})
        if existing_metadata:
            # Delete the existing image from GridFS and metadata collection
            existing_image_id = existing_metadata.get("image_id")
            if existing_image_id:
                try:
                    self.fs.delete(ObjectId(existing_image_id))
                except Exception as e:
                    logging.error(f"Error deleting existing image data: {e}")
            self.collection.delete_one({"image_name": image.image_name})

        # Save the new image data to GridFS
        image_id = self.fs.put(image.image_data, filename=image.image_name)

        # Save the new metadata to the metadata collection
        metadata = image.metadata or {}
        metadata.update({
            "image_id": str(image_id),
            "image_name": image.image_name
        })
        self.collection.insert_one(metadata)

        return str(image_id)

    def save_images(self, images: list[ImageEntity]) -> list[str]:
        """
        Save a list of images and their metadata to MongoDB.

        :param images: A list of ImageEntity objects.
        :return: A list of IDs of the saved images.
        """
        image_ids = []
        for image in images:
            image_id = self.save_image(image)
            image_ids.append(image_id)
        return image_ids

    def get_all_images(self) -> list[ImageEntity]:
        """
        Retrieve all images and their metadata from MongoDB.

        :return: A list of ImageEntity objects.
        """
        images = []
        # Retrieve all metadata from the metadata collection
        for metadata in self.collection.find():
            image_id = metadata.get("image_id")
            try:
                # Retrieve the image data from GridFS
                image_data = self.fs.get(ObjectId(image_id)).read()
                metadata.pop("_id", None)  # Remove the MongoDB internal ID
                images.append(ImageEntity(
                    image_name=metadata.get("image_name", "unknown"),
                    image_data=image_data,
                    metadata=metadata
                ))
            except Exception as e:
                logging.error(f"Error retrieving image with ID {image_id}: {e}")
        return images
