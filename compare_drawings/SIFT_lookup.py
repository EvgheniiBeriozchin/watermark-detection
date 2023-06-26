
import os
import cv2
import numpy as np
import pickle
import time
import sys, getopt
import matplotlib.pyplot as plt
from scipy.cluster.vq import vq
from SIFT_computeFeatures import computeFeatures
from SIFT_computeDistances import computeDistances


def SIFT_lookup(img_path, codebook, fv, images):

    # Load image from path
    image = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)

    # Compute features
    newfeat = computeFeatures(image)
    # Allocate features to fields from codebook
    code, distortion = vq(newfeat, codebook)
    # Map features to label and obtain BoW
    k = codebook.shape[0]
    # Create histogram from allocated keypoint features
    bow_hist, _ = np.histogram(code, k, density=True)
    # Update newfeat to BoW
    newfeat = bow_hist
    # insert new feat to the top of the feature vector stack
    fv = np.insert(fv, 0, newfeat, axis=0)
    # find all pairwise distances
    D = computeDistances(fv)
    # access distances of all images from query image (first image), sort them asc
    nearest_idx = np.argsort(D[0, 1:])
    # Change nearest index to list
    nss_list = np.ndarray.tolist(nearest_idx)
    #list_without_first_entry = nss_list[1:]
    #nss_list_new = [x - 1 for x in nss_list]
    # Get nns_names to nns
    nns_names = sorted(images, key=lambda i: nss_list.index(images.index(i)))
    return nss_list, nns_names