

import numpy as np
from computeFeatures import computeFeatures
from computeDistances import computeDistances
from scipy.cluster.vq import vq

def Find_nearest_index(img, codebook, fv):
    # empty list for holding features
    featvect = []
    # Compute features
    newfeat = computeFeatures(img)
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
    nearest_idx = np.argsort(D[0, :])
    # Change nearest index to list
    nearest_idx_list = np.ndarray.tolist(nearest_idx)

    return nearest_idx_list