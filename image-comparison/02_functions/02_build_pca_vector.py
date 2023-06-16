"""02_build_PCA_vector_for_PGA.ipynb


import os
import keras
import keras.utils as image
from keras.applications.imagenet_utils import decode_predictions, preprocess_input
from keras.models import Model
import cv2 as cv
from PIL import Image, ImageDraw
import numpy as np
from sklearn.decomposition import PCA
import time

def build_PCA_vector(images_path):
  # Load model
  model = keras.applications.VGG16(weights='imagenet', include_top=True)
  feat_extractor = Model(inputs=model.input, outputs=model.get_layer("fc2").output)

  # Pre sort images
  image_extensions = ['.jpg', '.png', '.jpeg']   # case-insensitive (upper/lower doesn't matter)
  max_num_images = 10000

  images = [os.path.join(dp, f) for dp, dn, filenames in os.walk(images_path) for f in filenames if os.path.splitext(f)[1].lower() in image_extensions]
  if max_num_images < len(images):
      images = [images[i] for i in sorted(random.sample(xrange(len(images)), max_num_images))]


  # Build image loader
  def load_image(path):
    img = image.load_img(path, target_size=model.input_shape[1:3])
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return img, x

  # Extract features from model
  tic = time.time()
  features = []
  for i, image_path in enumerate(images):
      if i % 500 == 0:
          toc = time.time()
          elap = toc-tic;
          print("analyzing image %d / %d. Time: %4.4f seconds." % (i, len(images),elap))
          tic = time.time()
      img, x = load_image(image_path);
      feat = feat_extractor.predict(x)[0]
      features.append(feat)

  # Extract 300 PCA features
  features = np.array(features)
  pca = PCA(n_components=300)
  pca.fit(features)

  pca_features = pca.transform(features)

  return pca_features