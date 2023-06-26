

# Load packages
import os
from PIL import Image
from torchvision import models, transforms
import torch.nn as nn
from annoy import AnnoyIndex
import time
import glob

def build_annoy_index(images_path):
  # Get images
  images = glob.glob(images_path + '/**/*.png', recursive=True)

  # Load model
  weights = models.ResNet18_Weights.IMAGENET1K_V1
  model = models.resnet18(weights=weights)
  model.fc = nn.Identity()
  model.eval()

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
      image = Image.open(os.path.join(images_path, images[i])).convert('RGB')
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

  return annoy_index, images
