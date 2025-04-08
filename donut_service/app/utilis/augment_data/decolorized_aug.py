from PIL import Image
from augment import DataAugmentation

class DecolorizedDataAugmentation(DataAugmentation):

    def __init__(self, json_path):
        super().__init__(json_path)
        self.name = "decolorized"
    
    def aug_image(self, image: Image):
        if image.mode != 'L':
            return None
        decolorized_image = image.convert("L")
        decolorized_image = decolorized_image.convert("RGB")
        return decolorized_image