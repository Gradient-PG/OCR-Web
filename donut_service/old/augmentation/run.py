from augment import DataAugmentation
from change_color_aug import ChangeColorDataAugmentation
from decolorized_aug import DecolorizedDataAugmentation
from edge_enhanced_aug import EdgeEnhancedDataAugmentation
from rotate_aug import RotateDataAugmentation
from salient_edge_map_aug import SalientEdgeMapDataAugmentation
from add_noise import process_images
import os


if not os.path.exists('labels/augmented'):
    os.makedirs('labels/augmented')

if not os.path.exists('images/aug'):
    os.makedirs('images/aug')

# augment data
a = DataAugmentation()
a.augment()
a = ChangeColorDataAugmentation()
a.augment()
a = DecolorizedDataAugmentation()
a.augment()
a = EdgeEnhancedDataAugmentation()
a.augment()
a = RotateDataAugmentation()
a.augment()
a = SalientEdgeMapDataAugmentation()
a.augment()


# add noise to images
process_images("images/aug", "images/aug")