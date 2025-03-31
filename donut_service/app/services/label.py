from app.entity.label import LabelEntity, to_st_field
from app.model.label import LabelRequest
from app.repository.mongodb.label import LabelRepository
import logging

class LabelService:
    def __init__(self, label_repository: LabelRepository):
        self.label_repository = label_repository

    def create_label_entity(self, request: LabelRequest) -> LabelEntity:
        """
        Converts a LabelRequest object into a LabelEntity object.
        """
        return LabelEntity(
            image_code=request.image_code,
            surname=request.surname,
            name=request.name,
            date_of_birth=request.date_of_birth,
            iii_st=to_st_field(request.iii_st),
            ii_st=to_st_field(request.ii_st),
            i_st=to_st_field(request.i_st),
            duplicate=request.duplicate
        )

    def save_label(self, label: LabelEntity):
        """
        Saves the label to the database. If a label with the same image_code exists,
        it updates the existing label; otherwise, it creates a new one.
        """
        # Check if a label with the given image_code exists
        existing_label = self.label_repository.get_label(label.image_code)
        if existing_label:
            # Update the existing label
            self.label_repository.update_label(label.image_code, label)
        else:
            # Create a new label
            self.label_repository.create_label(label)
        
    def get_labels(self):
        """
        Retrieves all labels from the database.
        """
        return self.label_repository.get_all_labels()
    
    