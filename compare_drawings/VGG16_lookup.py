

# Import packages
import os
import keras
import keras.utils as image
from keras.applications.imagenet_utils import decode_predictions, preprocess_input
from keras.models import Model
import cv2 as cv
from PIL import Image, ImageDraw
from scipy.stats import bernoulli
from scipy.spatial import distance
from sklearn.decomposition import PCA
from scipy.spatial import distance
import numpy as np
from VGG16_load_image import load_image


def Get_nns_VGG16(img_path,images,pca_features,pca):
    # Load model
    model = keras.applications.VGG16(weights='imagenet', include_top=True)
    feat_extractor = Model(inputs=model.input, outputs=model.get_layer("fc2").output)
    # Load image
    img, x = load_image(img_path,model)
    # Extract new features from
    new_features = feat_extractor.predict(x)
    new_pca_features = pca.transform(new_features)[0]
    distances = [ distance.cosine(new_pca_features, feat) for feat in pca_features ]
    nns = sorted(range(len(distances)), key=lambda k: distances[k])
    nns_names = sorted(images, key=lambda i: nns.index(images.index(i)))
    return nns, nns_names

