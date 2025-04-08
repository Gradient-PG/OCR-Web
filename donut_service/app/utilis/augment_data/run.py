import argparse
import shutil
from augment import DataAugmentation
from change_color_aug import ChangeColorDataAugmentation
from decolorized_aug import DecolorizedDataAugmentation
from edge_enhanced_aug import EdgeEnhancedDataAugmentation
from rotate_aug import RotateDataAugmentation
from salient_edge_map_aug import SalientEdgeMapDataAugmentation
from add_noise import process_images
import os

# Add argument parser
parser = argparse.ArgumentParser(description='Augment data from a JSON file')
parser.add_argument('json_path', type=str, help='Path to the input JSON file (e.g., labels/output_no_aug.json)')
args = parser.parse_args()

# backup original json_path
shutil.copy(args.json_path, args.json_path + '.bak')

# augment data with json path parameter
augmentation_classes = [
    DataAugmentation,
    ChangeColorDataAugmentation,
    DecolorizedDataAugmentation,
    EdgeEnhancedDataAugmentation,
    RotateDataAugmentation,
    SalientEdgeMapDataAugmentation
]

for AugClass in augmentation_classes:
    augmenter = AugClass(args.json_path)
    augmenter.augment()

# add noise to images
process_images("images/aug", "images/aug")