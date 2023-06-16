# -*- coding: utf-8 -*-
"""04_VGG16_lookup.ipynb


from sklearn.decomposition import PCA
from scipy.spatial import distance
import numpy as np

def Get_nns_VGG16(x,pca_features):
    new_features = feat_extractor.predict(x)
    new_pca_features = pca.transform(new_features)[0]
    distances = [ distance.cosine(new_pca_features, feat) for feat in pca_features ]
    nns = sorted(range(len(distances)), key=lambda k: distances[k])

    return nns
