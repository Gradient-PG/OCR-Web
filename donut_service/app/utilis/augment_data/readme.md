# Data Augmentation Guide

This tool provides various image augmentation techniques to enhance your dataset.

## Prerequisites

- Python 3.x
- Required Python packages: PIL (Pillow), numpy

## Setup

1. Place your original images in the `images` directory
2. First, run the labels processing script to generate the initial JSON file:
   ```bash
   python3 scripts/labels_processing.py no
   ```
   This will create `labels/output_no_aug.json` file with the image metadata.

## Running Augmentation

Run the augmentation script with the generated JSON file:

```bash
python3 scripts/augment_data/run.py labels/output_no_aug.json
```

**Important**: Before running any augmentations, the script will automatically create a backup of your original JSON file with `.bak` suffix (example: `labels/output_no_aug.json.bak`). This allows you to restore the original data if needed.

## Available Augmentations

The script will apply the following augmentations to your images:
- Color changes
- Decolorization
- Edge enhancement
- Rotation
- Salient edge mapping

Also, noise is added to all augumented images.

## Output

- Augmented images will be saved in the `images/aug` directory
- A backup of your original JSON file will be created as `labels/output_no_aug.json.bak`
- The JSON file will be updated with augmentation information for each image

## Restoring Original Data

If you need to restore the original data, simply copy the backup file:
```bash
cp labels/output_no_aug.json.bak labels/output_no_aug.json
```
