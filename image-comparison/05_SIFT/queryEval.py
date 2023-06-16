import os
import cv2
import numpy as np
import pickle
import time
import sys, getopt
import matplotlib.pyplot as plt
from scipy.cluster.vq import vq
from computeFeatures import computeFeatures, computeFeatures_baseline
from computeDistances import computeDistances



# Set up path
#dbpath = '/Users/sebastianpfaff/Documents/Studium/02_TUM/6. Semester/01_TUM Data Innovation Lab/13_Test_briquet/04_SIFT/Train_data'
#imgpath = '/Users/sebastianpfaff/Documents/Studium/02_TUM/6. Semester/01_TUM Data Innovation Lab/13_Test_briquet/04_SIFT/Train_data/500.jpg'
#queryfile = '/Users/sebastianpfaff/Documents/Studium/02_TUM/6. Semester/01_TUM Data Innovation Lab/13_Test_briquet/04_SIFT/Train_data/500.jpg'
dbpath = '/Users/sebastianpfaff/Documents/Studium/02_TUM/6. Semester/01_TUM Data Innovation Lab/13_Test_briquet/01_Test_dataset/02_Test_1000_images/TestImages2'


#Number of images
Nr_img = 1000

# create a arrays for precision and recall
precision_bow = []
precision_tfidf = []
precision_base = []
recall_bow = []
recall_tfidf = []
recall_base = []

# Set up query file

# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"d:q:h")
print(myopts)
# parsing command line args
for o, a in myopts:
    if o == '-d':
        queryfile = os.path.join(dbpath, a + '.jpg')
        if not os.path.isfile(queryfile):
            print("Error: Query file does not exist! Please check.")
            sys.exit()
    elif o == '-q':
        queryfile = a
        if not os.path.isfile(queryfile):
            print("Error: Query file does not exist! Please check.")
            sys.exit()
        # tokenize filename to get category label and index
        gt = str(queryfile.split("_")[1]).split(".")[0]
    elif o == '-h':
        print("\nUsage: %s -d dbfilenumber\n       # to specify a single query image from the database for evaluation" % sys.argv[0])
        print("\n       %s -q queryfile\n       # to specify a new query image for evaluation" % sys.argv[0])
        print(" ")
        sys.exit()
    else:
        print(' ')

# read query image file
img = cv2.imread(queryfile)
query_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


plt.figure("Query Image")
# show stuff
plt.imshow(query_img), plt.title('Query image: %s')
plt.imshow(query_img), plt.title('Query image')
plt.xticks([]), plt.yticks([])
print('Query image: %s')
print("")

e0 = time.time()


#====================================================================
# Bag-of-word Features
#====================================================================

featvect = []  # empty list for holding features
FEtime = np.zeros(Nr_img)

# load pickled features
fv = pickle.load(open("bow.pkl", "rb") )
print('BoW features loaded')

# Compute features
newfeat = computeFeatures(query_img)
# Load cookbook
codebook = pickle.load(open("codebook.pkl", "rb"))
code, distortion = vq(newfeat, codebook)
# Map features to label and obtain BoW
k = codebook.shape[0]
bow_hist, _ = np.histogram(code, k, density=True)
# Update newfeat to BoW
newfeat = bow_hist


# insert new feat to the top of the feature vector stack
fv = np.insert(fv, 0, newfeat, axis=0)

# find all pairwise distances
D = computeDistances(fv)


# *** Evaluation ----------------------------------------------------------

# number of images to retrieve
nRetrieved = 10

# access distances of all images from query image (first image), sort them asc
nearest_idx = np.argsort(D[0, :]);

# *** Results & Visualization-----------------------------------------------


print('position of real images:')
print(np.where(nearest_idx == a))

print('================================')
print('           Bag-of-word')
print('================================')



fig, axs = plt.subplots(2, 5, figsize=(15, 6), facecolor='w', edgecolor='w', num='Bag-of-word')
fig.subplots_adjust(hspace = .5, wspace=.001)
fig.suptitle('Bag-of-word', fontsize=16)
axs = axs.ravel()
#to calculate how many match image for precision = match / return
match_precision=0
for i in range(10):
    imgfile = os.path.join(dbpath, str(nearest_idx[i+1]) + '.jpg')
    matched_img = cv2.cvtColor(cv2.imread(imgfile), cv2.COLOR_BGR2RGB)
    axs[i].imshow(matched_img)
    axs[i].set_title(str(i+1))
    axs[i].set_xticks([])
    axs[i].set_yticks([])

#print(precision_bow)
print("")
#print(recall_bow)
print("")


#====================================================================
# TD-IDF Features
#====================================================================

featvect = []  # empty list for holding features
FEtime = np.zeros(Nr_img)

# load pickled features
fv = pickle.load(open("tfidf.pkl", "rb") )
print('TF-IDF features loaded')

# read query image file
img = cv2.imread(queryfile)
query_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


# Compute features
newfeat = computeFeatures(query_img)
# Load cookbook
codebook = pickle.load(open("codebook.pkl", "rb"))
code, distortion = vq(newfeat, codebook)
# Map features to label and obtain BoW
k = codebook.shape[0]
bow_hist, _ = np.histogram(code, k, density=True)
# Update newfeat to BoW
newfeat = bow_hist


# insert new feat to the top of the feature vector stack
fv = np.insert(fv, 0, newfeat, axis=0)

# find all pairwise distances
D = computeDistances(fv)



# *** Evaluation ----------------------------------------------------------

# number of images to retrieve
nRetrieved = 10

# access distances of all images from query image (first image), sort them asc
nearest_idx = np.argsort(D[0, :]);

#for curve  Nr_img
retrievedCurve = np.uint8(np.floor(((nearest_idx[1:Nr_img+1])-1)/10));

# *** Results & Visualization-----------------------------------------------

print('================================')
print('              TF-IDF')
print('================================')


fig, axs = plt.subplots(2, 5, figsize=(15, 6), facecolor='w', edgecolor='w', num='TF-IDF')
fig.subplots_adjust(hspace = .5, wspace=.001)
fig.suptitle('TF-IDF', fontsize=16)
axs = axs.ravel()
#to calculate how many match image for precision = match / return
match_precision=0
for i in range(10):
    imgfile = os.path.join(dbpath, str(nearest_idx[i+1]) + '.jpg')
    matched_img = cv2.cvtColor(cv2.imread(imgfile), cv2.COLOR_BGR2RGB)
    axs[i].imshow(matched_img)
    axs[i].set_title(str(i + 1))
    axs[i].set_xticks([])
    axs[i].set_yticks([])
  


#print(precision_tfidf)
#print("")
#print(recall_tfidf)
print("")

e1 = time.time()
print('Total time:')
print(e1-e0)

plt.show()




