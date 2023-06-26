"""
SIFT_exctract_features.py


"""
import cv2
import numpy as np
import pickle
import time
from scipy.cluster.vq import kmeans, vq
from SIFT_computeFeatures import computeFeatures
import glob
import os

def SIFT_exctract_features(images_path, k_means = 50, save_features = False):
    # Images
    images = glob.glob(images_path + '/**/*.png', recursive=True)
    # List of features that stores
    feat = []
    base_feat = []

    # Start timing
    t0 = time.time()

    for i, image_path in enumerate(images):
        # Load and convert image
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Compute SIFT features for each keypoints
        feat.append(computeFeatures(img))

        print('Extracting features for image #%d' % i)

    # Stack all features together
    alldes = np.vstack(feat)

    # Perform K-means clustering
    alldes = np.float32(alldes)  # convert to float, required by kmeans and vq functions
    e0 = time.time()
    codebook, distortion = kmeans(alldes, k_means, iter=1, thresh=1e-05, seed=3)
    code, distortion = vq(alldes, codebook)
    e1 = time.time()
    print("Time to build {}-cluster codebook from {} images: {} seconds".format(k_means, alldes.shape[0], e1 - e0))

    ##############################################################################

    # ====================================================================
    # Bag-of-word Features
    # ====================================================================
    # Create Bag-of-word list
    bow = []

    # Get label for each image, and put into a histogram (BoW)
    for f in feat:
        code, distortion = vq(f, codebook)
        bow_hist, _ = np.histogram(code, k_means, density=True)
        bow.append(bow_hist)

    # Stack them together
    temparr = np.vstack(bow)

    # Put them into feature vector
    fv = np.reshape(temparr, (temparr.shape[0], temparr.shape[1]))
    del temparr

    return codebook, fv, images
