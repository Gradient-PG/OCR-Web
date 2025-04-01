from bson import ObjectId
from app.entity.label import LabelEntity, to_st_field
from pymongo import MongoClient
import os

class LabelRepository:
    def __init__(self, database_name="donut_service_database"):
        self.client = MongoClient(
            host=os.getenv("MONGO_HOST", "mongodb"),
            port=int(os.getenv("MONGO_PORT", 27017)),
            username=os.getenv("MONGO_USER", "root"),
            password=os.getenv("MONGO_PASS", "pass"),
        )
        self.db = self.client[database_name]
        self.collection = self.db["labels"]

    def get_label(self, image_code: str) -> LabelEntity:
        """
        Fetch a label by its image_code and return it as a LabelEntity.
        """
        try:
            document = self.collection.find_one({"image_code": image_code})
            if not document:
                return None
            gt_parse = document.get("gt_parse", {})
            return LabelEntity(
                image_code=document["image_code"],
                surname=gt_parse.get("Surname"),
                name=gt_parse.get("Name"),
                date_of_birth=gt_parse.get("Date of birth"),
                iii_st=to_st_field(gt_parse.get("III st.")),
                ii_st=to_st_field(gt_parse.get("II st.")),
                i_st=to_st_field(gt_parse.get("I st.")),
                duplicate=gt_parse.get("Duplicate"),
            )
        except Exception as e:
            raise ValueError(f"Error fetching label with image_code {image_code}: {str(e)}") from e
        
    def update_label(self, image_code: str, label: LabelEntity):
        """
        Update an existing label by its image_code.
        """
        try:
            label_data = label.to_dict()  # Convert LabelEntity to a dictionary
            result = self.collection.update_one(
                {"image_code": image_code}, {"$set": label_data}
            )
            if result.matched_count == 0:
                raise ValueError(f"Label with image_code {image_code} not found.")
            return result.modified_count
        except Exception as e:
            raise ValueError(f"Error updating label with image_code {image_code}: {str(e)}") from e

    def create_label(self, label: LabelEntity) -> str:
        """
        Create a new label and return its ID.
        """
        label_data = label.to_dict()  # Convert LabelEntity to a dictionary
        result = self.collection.insert_one(label_data)
        return str(result.inserted_id)

    def get_all_labels(self) -> list:
        """
        Fetch all labels from the database.
        """
        documents = self.collection.find()
        labels = []
        for document in documents:
            gt_parse = document.get("gt_parse", {})
            labels.append(
                LabelEntity(
                    image_code=document["image_code"],
                    surname=gt_parse.get("Surname"),
                    name=gt_parse.get("Name"),
                    date_of_birth=gt_parse.get("Date of birth"),
                    iii_st=to_st_field(gt_parse.get("III st.")),
                    ii_st=to_st_field(gt_parse.get("II st.")),
                    i_st=to_st_field(gt_parse.get("I st.")),
                    duplicate=gt_parse.get("Duplicate"),
                )
            )
        return labels