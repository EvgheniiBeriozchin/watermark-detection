# This function returns the vector of PCA features extracted from images using the VGG16 model.


# Import packages
import glob
import keras
from keras.applications.imagenet_utils import decode_predictions
from keras.models import Model
import numpy as np
from sklearn.decomposition import PCA
import time
from VGG16_load_image import load_image
import pickle
import os

FEATURE_DATABASE_PATH = "../../data/image-database/"

def build_PCA_vector(images_path, save_features = False):
  '''
  Input:
  images_path: folder path of images for which the features should be extracted.
  The features are also extracted for all subfolders

  Output:
  images: pathname of images
  pca_features: pca_features of the images
  PCA: information on the PCA performed
  '''

  # Load model and set up feature extractor
  model = keras.applications.VGG16(weights='imagenet', include_top=True)
  feat_extractor = Model(inputs=model.input, outputs=model.get_layer("fc2").output)

  # Load images from path
  images = glob.glob(images_path + '/**/*.png', recursive=True)

  # Extract features from model and save them in list feat
  tic = time.time()
  features = []
  for i, image_path in enumerate(images):
      if i % 500 == 0:
          toc = time.time()
          elap = toc-tic;
          print("analyzing image %d / %d. Time: %4.4f seconds." % (i, len(images),elap))
          tic = time.time()
      img, x = load_image(image_path,model);
      feat = feat_extractor.predict(x)[0]
      features.append(feat)

  # Extract 300 PCA features to reduce dimension
  features = np.array(features)
  pca = PCA(n_components=300)
  pca.fit(features)

  pca_features = pca.transform(features)

  # Save featrues
  if save_features == True:
      save_path = os.path.join(FEATURE_DATABASE_PATH, 'VGG16_features.pkl')
      pickle.dump([images, pca_features, pca], open(save_path, 'wb'))

  # Return image names, pca_features and pca
  return images, pca_features, pca

