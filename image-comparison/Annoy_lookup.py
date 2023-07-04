
import torch
from torchvision import models, transforms
import torch.nn as nn
import numpy as np
from annoy import AnnoyIndex
from PIL import Image, ImageDraw


def Get_nns_spotify_annoy(image_path,annoy_index, images):

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
        ])

    weights = models.ResNet18_Weights.IMAGENET1K_V1
    model = models.resnet18(weights=weights)
    model.fc = nn.Identity()
    model.eval()

    image = Image.open(image_path).convert('RGB')

    input_tensor = transform(image).unsqueeze(0)
    output_tensor = model(input_tensor)
    nns = annoy_index.get_nns_by_vector(output_tensor[0],1000)
    nns_names = sorted(images, key=lambda i: nns.index(images.index(i)))

    return nns, nns_names