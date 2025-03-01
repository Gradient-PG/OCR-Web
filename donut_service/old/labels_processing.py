#!/usr/bin/env python
# coding: utf-8
import os
import json
import copy
from utils.labels_processing import get_processed_all
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('augmentation', type=str, help='include augmented data')

args = parser.parse_args()

if args.augmentation == 'no':
  output = get_processed_all('labels/raw_proper/')

  with open(f"labels/processed/output_no_aug.json", "w", encoding='utf8') as outfile: 
    json.dump(output, outfile, ensure_ascii=False)


#augmented output
elif args.augmentation == 'aug':
  output = get_processed_all('labels/augmented/', aug=True)

  with open(f"labels/processed/output.json", "w", encoding='utf8') as outfile: 
    json.dump(output, outfile, ensure_ascii=False)


  # image_dic = {}
  # for image in os.listdir(f"images/aug/"):

  #   name_image = image.split('_')
  #   # if name_image[0] == 'original':
  #   #   continue

  #   if len(name_image) == 3:
  #     name_image = name_image[2]
  #   elif len(name_image) == 4:
  #     name_image = name_image[3]
  #   else:
  #     name_image = name_image[1]
    

  #   if name_image in image_dic.keys():
  #     image_dic[name_image].append(image) 
  #   else:
  #     image_dic.update({f"{name_image}":[]})
  #     image_dic[name_image].append(image)

  # raw_output = copy.deepcopy(output)

  # for i,j_file in enumerate(raw_output):

  #   image_code = j_file['image_code']
  #   for name_image in image_dic[image_code]:

  #     if 'original' in name_image:
  #       output[i]['image_code'] = f'original_{image_code}'
  #     else:
  #       c_file = j_file
  #       c_file['image_code'] = name_image
  #       output.append(c_file)

  # with open(f"labels/processed/output_aug.json", "w", encoding='utf8') as outfile: 
  #   json.dump(output, outfile, ensure_ascii=False)