"""
featureExtraction.py


"""
import os
import cv2
import numpy as np
import pickle
import matplotlib.pyplot as plt
import time
from scipy.cluster.vq import kmeans, vq
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfTransformer
from computeFeatures import computeFeatures, computeFeatures_baseline

# EDIT THIS TO YOUR OWN PATH IF DIFFERENT
dbpath = '/Users/sebastianpfaff/Documents/Studium/02_TUM/6. Semester/01_TUM Data Innovation Lab/13_Test_briquet/01_Test_dataset/02_Test_1000_images/TestImages2'

##############################################################################

# List of features that stores
feat = []
base_feat = []

# Start timing
t0 = time.time()

for idx in range(1000):
    # Load and convert image
    img = cv2.imread(os.path.join(dbpath, str(idx+1) + ".jpg") )
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Compute SIFT features for each keypoints
    feat.append(computeFeatures(img))

    # Compute baseline features for each image
    base_feat.append(computeFeatures_baseline(img))

    print('Extracting features for image #%d'%idx )

# Stack all features together
alldes = np.vstack(feat)

k = 50

# Perform K-means clustering
alldes = np.float32(alldes)      # convert to float, required by kmeans and vq functions
e0 = time.time()
codebook, distortion = kmeans(alldes, k, iter=1, thresh=1e-05, seed = 3)
code, distortion = vq(alldes, codebook)
e1 = time.time()
print("Time to build {}-cluster codebook from {} images: {} seconds".format(k,alldes.shape[0],e1-e0))

# Save codebook as pickle file
pickle.dump(codebook, open("codebook.pkl", "wb"))



# Load cookbook
codebook = pickle.load(open("codebook.pkl", "rb"))

##############################################################################

#====================================================================
# Bag-of-word Features
#====================================================================
# Create Bag-of-word list
bow = []

# Get label for each image, and put into a histogram (BoW)
for f in feat:
    code, distortion = vq(f, codebook)
    bow_hist, _ = np.histogram(code, k, density=True)
    bow.append(bow_hist)
    
# Stack them together
temparr = np.vstack(bow)

# Put them into feature vector
fv = np.reshape(temparr, (temparr.shape[0], temparr.shape[1]) )
del temparr


# pickle your features (bow)
pickle.dump(fv, open("bow.pkl", "wb"))
print('')
print('Bag-of-words features pickled!')

#====================================================================
# TF-IDF Features
#====================================================================
def tfidf(bow):
	# td-idf weighting
    transformer = TfidfTransformer(smooth_idf=True)
    t = transformer.fit_transform(bow).toarray()
        
    # normalize by Euclidean (L2) norm before returning 
    t = normalize(t, norm='l2', axis=1)
    
    return t

# re-run vq without normalization, normalize after computing tf-idf
bow = np.vstack(bow)
t = tfidf(bow)

# pickle your features (tfidf)
pickle.dump(t, open("tfidf.pkl", "wb"))
print('TF-IDF features pickled!')

#====================================================================
# Baseline Features
#====================================================================
# Stack all features together
base_feat = np.vstack(base_feat)


# pickle your features (baseline)
pickle.dump(base_feat, open("base.pkl", "wb"))
print('Baseline features pickled!')

# Finish timing
t1 = time.time()
print('Total time:')
print(t1-t0)


#====================================================================
