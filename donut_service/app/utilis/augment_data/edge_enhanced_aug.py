from PIL import Image, ImageFilter
from augment import DataAugmentation

class EdgeEnhancedDataAugmentation(DataAugmentation):

    def __init__(self, json_path):
        super().__init__(json_path)
        self.name = "edge_enhance"
    
    def aug_image(self, image: Image):
        if image.mode != 'RGB': 
            image = image.convert('RGB') 
        enhanced_image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return enhanced_image