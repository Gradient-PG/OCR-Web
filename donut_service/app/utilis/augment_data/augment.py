import json
import os
from PIL import Image
from typing import List

class DataAugmentation:
    """Base class for image data augmentation operations.
    
    Attributes:
        json_path (str): Path to the JSON file containing image metadata
        name (str): Name of the augmentation technique
        json_data (dict): Loaded JSON data
        input_image_dir (str): Directory containing input images
        output_image_dir (str): Directory for augmented images
    """

    def __init__(self, json_path):
        self.json_path = json_path
        # override this name for new DataAugmentation
        self.name = "original"
        self.json_data = None
        # Add base paths as class attributes
        self.input_image_dir = os.path.join('images')
        self.output_image_dir = os.path.join('images', 'aug')
        # Ensure output directory exists
        os.makedirs(self.output_image_dir, exist_ok=True)
        
    def augment(self):
        print("Start augmentation for " + self.name)
        
        try:
            # Load JSON data once at the start
            with open(self.json_path, 'r', encoding='utf-8') as file:
                self.json_data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading JSON file: {e}")
            return
        
        if not self.validate_json_data():
            return
        
        list_of_img_name = self.load_images_from_jsons()
        if not list_of_img_name:
            print("No images found in JSON data")
            return
        
        for img_name in list_of_img_name:
            try:
                img_path = os.path.join(self.input_image_dir, img_name)
                with Image.open(img_path) as img:
                    img = self.aug_image(img)
                    if img is None:
                        print(f"Error: Augmentation failed for {img_name}")
                        continue
                    
                    self.save_image(img, img_name)
                    self.aug_json(img_name)
            except Exception as e:
                print(f"Error: Augmentation failed for {img_name} with error: {str(e)}")
                continue
        
        # Save JSON data once at the end
        with open(self.json_path, 'w', encoding='utf-8') as file:
            json.dump(self.json_data, file, indent=4, ensure_ascii=False)
            
        print("End augmentation for " + self.name)

    def load_images_from_jsons(self) -> List[str]:
        """Extract image filenames from JSON data.
        
        Returns:
            List of image filenames
        """
        return [image["image_code"] for image in self.json_data]

    def save_image(self, image, img_name):
        output_path = os.path.join(self.output_image_dir, f"{self.name}_{img_name}")
        image.save(output_path)

    # override this method
    def aug_image(self, image):
        """Apply augmentation to the image.
        
        Args:
            image: PIL Image to augment
            
        Returns:
            Augmented image or None if augmentation fails
        """
        return image

    def aug_json(self, image_name):
        for image in self.json_data:
            image_code = image["image_code"]
            if image_code == image_name:
                if "aug" not in image:
                    image["aug"] = []
                if self.name not in image["aug"] and self.name != "original":
                    image["aug"].append(self.name)

    def validate_json_data(self) -> bool:
        """Validate the structure of loaded JSON data.
        
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(self.json_data, list):
            print("Error: JSON data must be a list")
            return False
        
        for item in self.json_data:
            if not isinstance(item, dict):
                print("Error: Each JSON item must be a dictionary")
                return False
            if "image_code" not in item:
                print("Error: Missing 'image_code' in JSON item")
                return False
        return True