from PIL import Image
import random
from augment import DataAugmentation


class ChangeColorDataAugmentation(DataAugmentation):
    
    def __init__(self, json_path):
        super().__init__(json_path)
        self.name = "change_color"
        
    def aug_image(self, image):
        if image.mode != 'RGB': 
            image = image.convert('RGB') 
        new_channels = []
        channels = image.split()
        for channel in channels:
            if 0.5 < random.random():
                rand_num = random.randrange(-60, -25)
            else:
                rand_num = random.randrange(25, 60)
            new_channels.append(channel.point(lambda x: x + rand_num))
        augmented_image = Image.merge('RGB', tuple(new_channels))
        return augmented_image