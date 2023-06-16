# -*- coding: utf-8 -*-
"""03_build_annoy_index.ipynb


!pip install annoy

import os
from PIL import Image, ImageDraw
import torch
from torchvision import models, transforms
import torch.nn as nn
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
from annoy import AnnoyIndex
import time

def build_annoy_index(images_path, model):
  # Define transform
  transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
    ])

  # Build annoy index
  annoy_index = AnnoyIndex(512, 'angular')

  # Extract features from model
  t0 = time.time()
  for i in range(len(images)):
      image = Image.open(os.path.join(images_folder, images[i])).convert('RGB')
      input_tensor = transform(image).unsqueeze(0)
      if input_tensor.size()[1] == 3:
          output_tensor = model(input_tensor)
          annoy_index.add_item(i, output_tensor[0])
          if i % 100 == 0:
              print(f'Processed { i } images.')
  t1 = time.time()
  print(t1-t0)

  # build index
  annoy_index.build(10)

  return annoy_index