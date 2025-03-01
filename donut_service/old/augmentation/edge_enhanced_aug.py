from PIL import Image, ImageFilter
from augment import DataAugmentation

class EdgeEnhancedDataAugmentation(DataAugmentation):

    def __init__(self):
        self.name = "edge_enhance"
    
    def aug_image(self, image: Image):
        enhanced_image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return enhanced_image