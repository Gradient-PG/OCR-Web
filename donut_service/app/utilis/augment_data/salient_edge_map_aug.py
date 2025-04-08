from PIL import Image, ImageFilter
import numpy as np
from augment import DataAugmentation


class SalientEdgeMapDataAugmentation(DataAugmentation):

    def __init__(self, json_path):
        super().__init__(json_path)
        self.name = "salient_edge_map"
    
    def aug_image(self, image: Image):
        if image.mode != 'L': 
            image = image.convert('L') 
        gray_array = np.array(image)

        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=2))
        blurred_array = np.array(blurred_image)

        edge_map = np.clip(gray_array - blurred_array, 0, 255).astype(np.uint8)

        return Image.fromarray(edge_map)