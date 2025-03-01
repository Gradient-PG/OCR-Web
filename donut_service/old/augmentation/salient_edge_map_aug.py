from PIL import Image, ImageFilter
import numpy as np
from augment import DataAugmentation


class SalientEdgeMapDataAugmentation(DataAugmentation):

    def __init__(self):
        self.name = "salient_edge_map"
    
    def aug_image(self, image: Image):
        gray_image = image.convert("L")
        gray_array = np.array(gray_image)

        blurred_image = gray_image.filter(ImageFilter.GaussianBlur(radius=2))
        blurred_array = np.array(blurred_image)

        edge_map = np.clip(gray_array - blurred_array, 0, 255).astype(np.uint8)

        return Image.fromarray(edge_map)