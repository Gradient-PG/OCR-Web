from PIL import Image
from augment import DataAugmentation

class DecolorizedDataAugmentation(DataAugmentation):

    def __init__(self):
        self.name = "decolorized"
    
    def aug_image(self, image: Image):
        decolorized_image = image.convert("L")
        decolorized_image = decolorized_image.convert("RGB")
        return decolorized_image