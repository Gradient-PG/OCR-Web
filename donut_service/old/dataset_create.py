#!/usr/bin/env python
# coding: utf-8
import json
import numpy as np
from datasets import Dataset, Image
import sys

def prepare_dataset_dict(json_file, start_id):
  ds_dict = {
    "image": [],
    "ground_truth": []
  }
  
  for i, single_json in enumerate(json_file):
    image_name = single_json['image_code']
    ds_dict["image"].append(f"{IMAGES_DIR}/{image_name}")
    
    # single_json_copy = single_json.copy()
    # del single_json_copy['image_code']
    
    json_str = str(single_json).replace('\'', '\"')
    ds_dict["ground_truth"].append(json_str)
    
  return ds_dict


def to_rgb(elem):
  elem['image'] = elem['image'].convert("RGB")
  return elem


if len(sys.argv) == 1:
  IMAGES_DIR = 'images/aug/'
  file = open(f'labels/processed/output.json')
  dataset_name = f'{sys.argv[0]}_dataset'

json_file = json.load(file)
out_dict = prepare_dataset_dict(json_file, 101)

# from PIL import Image as ImagePIL
dataset = Dataset.from_dict(out_dict).cast_column("image", Image())

# this option is commented because augmentation already converts images to RGB
#
# dataset = dataset.map(to_rgb)

dataset.save_to_disk(f'datasets/{dataset_name}')
