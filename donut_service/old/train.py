from datasets import load_dataset, load_from_disk
from transformers import DonutProcessor, VisionEncoderDecoderConfig, VisionEncoderDecoderModel
import torch
import json
from torch.utils.data import Dataset
from typing import Any, List, Tuple
from torch.utils.data import DataLoader
import re
from nltk import edit_distance
import numpy as np
import pytorch_lightning as pl
import csv
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning.callbacks import Callback, EarlyStopping
from pytorch_lightning.loggers import CSVLogger
import argparse
import sys
import os
from donut_model_pl_module import DonutModelPLModule
from donut_dataset import DonutDataset

# from tqdm.auto import tqdm
# from donut import JSONParseEvaluator


parser = argparse.ArgumentParser(description='Create a folder with the specified name')
parser.add_argument('folder_name', type=str, help='Type in dataset name')

# Parse arguments
args = parser.parse_args()

# Create the folder with the given name
model_path = os.path.join('models', args.folder_name)

try:
    os.makedirs(model_path, exist_ok=True)
    print(f"Folder '{args.folder_name}' created at {model_path}")
except Exception as e:
    print(f"Error creating folder: {e}")

if os.path.exists(f'datasets/{args.folder_name}_dataset'):
    DATASET_PATH = f'datasets/{args.folder_name}_dataset'
else:
    print('Folder name and dataset name are different')
    sys.exit()


MODEL_TOKEN_START = "<ocr_pck>"
MODEL_TOKEN_END = '<ocr_pck/>'


torch.random.manual_seed(0)
torch.cuda.get_device_properties(0)


image_size = [1653, 1165]
max_length = 768

config = VisionEncoderDecoderConfig.from_pretrained("naver-clova-ix/donut-base")
config.encoder.image_size = image_size # (height, width)
# update max_length of the decoder (for generation)
config.decoder.max_length = max_length
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base", config=config)
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
processor.image_processor.size = image_size[::-1] # should be (width, height)
processor.image_processor.do_align_long_axis = False

donut_dataset = DonutDataset(processor, DATASET_PATH, max_length=max_length, task_start_token=MODEL_TOKEN_START, prompt_end_token=MODEL_TOKEN_END,
                              sort_json_key=False, # cord dataset is preprocessed, so no need for this
                            )

print(len(donut_dataset.gt_token_sequences), len(donut_dataset.dataset))


train_size = int(0.8 * len(donut_dataset))
# train_size = 50

val_size = len(donut_dataset) - train_size
# test_size = len(donut_dataset) - train_size

train_dataset, val_dataset = torch.utils.data.random_split(donut_dataset, [train_size, val_size])


val_dataset.split = "validation"


model.config.pad_token_id = processor.tokenizer.pad_token_id
model.config.decoder_start_token_id = processor.tokenizer.convert_tokens_to_ids([MODEL_TOKEN_START])[0]


dataloader_whole = DataLoader(donut_dataset, batch_size=2, shuffle=True)

train_dataloader = DataLoader(train_dataset, batch_size=2, shuffle=True,num_workers=31)
val_dataloader = DataLoader(val_dataset, batch_size=2, shuffle=False)
# test_dataloader = DataLoader(test_dataset, batch_size=2, shuffle=False)

config = {
    "max_epochs":1000,
    "val_check_interval":1.0, # how many times we want to validate during an epoch
    "check_val_every_n_epoch": 1,
    "gradient_clip_val":1.0,
    "lr":3e-5,
    "train_batch_sizes": [2],
    "val_batch_sizes": [2],
    "seed": 0,
    "num_nodes": 1,
    # "warmup_steps": 10, # 50/2*4/10, 10% # 800/8*30/10, 10%
    # "result_path": "./result",
    "verbose": True,
}

model_module = DonutModelPLModule(config, processor, model)

early_stop_callback = EarlyStopping(monitor="val_edit_distance", patience=20, verbose=False, mode="min")

logger = CSVLogger(model_path, name="logs")

trainer = pl.Trainer(
    accelerator="gpu",
    devices=1,
    max_epochs=config.get("max_epochs"),
    # val_check_interval=config.get("val_check_interval"),
    check_val_every_n_epoch=config.get("check_val_every_n_epoch"),
    # gradient_clip_val=config.get("gradient_clip_val"),
    precision='16-mixed', # we'll use mixed precision
    # num_sanity_val_steps=0,
    callbacks=[early_stop_callback],
    logger=logger
)

trainer.fit(model_module)
trainer.validate(model_module)


model.save_pretrained(model_path)
processor.save_pretrained(model_path)



torch.cuda.empty_cache()
torch.cuda.get_device_properties(0).total_memory
