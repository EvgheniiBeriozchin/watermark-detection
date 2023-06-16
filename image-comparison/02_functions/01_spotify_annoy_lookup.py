"""01_Spotify_annoy_lookup.ipynb

!pip install annoy

import torch
from torchvision import models, transforms
import torch.nn as nn
import numpy as np
from annoy import AnnoyIndex
from PIL import Image, ImageDraw
from PIL import Image, ImageDraw
import os

def Get_nns_spotify_annoy(image,annoy_index, model):

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
        ])

    input_tensor = transform(image).unsqueeze(0)
    output_tensor = model(input_tensor)
    nns = annoy_index.get_nns_by_vector(output_tensor[0],1000)

    return nns
