

import os
import pickle
import numpy as np
import time
import pandas as pd
from create_test_image import create_test_image
from Find_nearest_index import Find_nearest_index
import cv2
import matplotlib.pyplot as plt
from computeFeatures import computeFeatures
from computeDistances import computeDistances
from scipy.cluster.vq import vq



#dbpath = '/Users/sebastianpfaff/Documents/Studium/02_TUM/6. Semester/01_TUM Data Innovation Lab/13_Test_briquet/04_SIFT/Train_data'
dbpath = '/Users/sebastianpfaff/Documents/Studium/02_TUM/6. Semester/01_TUM Data Innovation Lab/13_Test_briquet/01_Test_dataset/02_Test_1000_images/TestImages Kopie'

dbpath = '/Users/sebastianpfaff/Documents/Studium/02_TUM/6. Semester/01_TUM Data Innovation Lab/13_Test_briquet/01_Test_dataset/02_Test_1000_images/TestImages2'

#Number of images
Nr_img = 1000


'''
img = cv2.imread(queryfile)
query_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
transform_img = create_test_image(query_img, 1)

plt.figure("Query Image")
plt.imshow(query_img)
'''


'''
#====================================================================
# Bag-of-word Features
#====================================================================

featvect = []  # empty list for holding features
FEtime = np.zeros(Nr_img)

# load pickled features
fv = pickle.load(open("bow.pkl", "rb") )
print('BoW features loaded')

# Compute features
newfeat = computeFeatures(transform_img)
# Load cookbook
codebook = pickle.load(open("codebook_2.pkl", "rb"))
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

print(nearest_idx)
'''
'''
imgfile = os.path.join(dbpath, str(nearest_idx[10]) + '.jpg')
matched_img = cv2.cvtColor(cv2.imread(imgfile), cv2.COLOR_BGR2RGB)
plt.figure("Matched Image")
plt.imshow(matched_img)
plt.show()
list_of_rows = []
'''
'''
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
'''

'''

true_imgfile = os.path.join(dbpath, str(nearest_idx[true_img_nr]) + '.jpg')
true_img = cv2.cvtColor(cv2.imread(true_imgfile), cv2.COLOR_BGR2RGB)
plt.figure("True Image")
plt.imshow(true_img)
plt.show()
print(true_img_nr)
'''





# load pickled features
import_fv = pickle.load(open("bow.pkl", "rb") )
print('BoW features loaded')


# Load cookbook
codebook = pickle.load(open("codebook.pkl", "rb"))
print('Codebook loaded')


images = os.listdir(dbpath)

list_of_rows = []

#Nr_img
for i in range(1, Nr_img+1):
    print(i)
    t0 = time.time()
    img_name = str(i) + '.jpg'
    img_path = os.path.join(dbpath,  str(i) + '.jpg')
    query_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    query_index = images.index(img_name)
    another_row = [str(i) + '.jpg']
    for j in range(1, 14):
        # Set fv new
        fv = import_fv
        # Transform image
        transform_img = create_test_image(query_img, j)
        # Compute features
        # empty list for holding features
        featvect = []
        # Compute features
        newfeat = computeFeatures(transform_img)
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
        # Find real image in list of nearest neighbours
        position = nearest_idx_list.index(i)
        # Add nearest neighbour for test image j of real image i to list
        another_row.append(position)
    if i % 10 == 0:
        t1 = time.time()
        print(f'{i} nearest neighbours calculated')
        print('Time for batch:')
        print(t1-t0)
    list_of_rows.append(another_row)

# Set up column
column_names = ['Name','Number1','Number2','Number3','Number4','Number5','Number6', \
                'Number7', 'Number8', 'Number9', 'Number10', 'Number11', 'Number12', 'Number13']

# Create a DataFrame
df = pd.DataFrame(list_of_rows, columns=column_names)
df.to_csv('Data_frame_test_results.csv')
# Print the DataFrame


'''
fv = import_fv
img_path = os.path.join(dbpath, "test_images_" + str(245) + '.png')
query_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
another_row = ["test_images_" + str(245) + '.png']
nearest_idx = Find_nearest_index(query_img, codebook, fv)
position = nearest_idx.index(245)
# Add nearest neighbour for test image j of real image i to list
another_row.append(position)
for j in range(1, 14):
    # Set fv new
    fv = import_fv
    # Transform image
    transform_img = create_test_image(query_img, j)
    # Compute features
    nearest_idx = Find_nearest_index(transform_img, codebook, fv)
    # Find real image in list of nearest neighbours
    position = nearest_idx.index(245)
    # Add nearest neighbour for test image j of real image i to list
    another_row.append(position)

print(nearest_idx)

fig, axs = plt.subplots(2, 5, figsize=(15, 6), facecolor='w', edgecolor='w', num='TF-IDF')
fig.subplots_adjust(hspace = .5, wspace=.001)
fig.suptitle('TF-IDF', fontsize=16)
axs = axs.ravel()
#to calculate how many match image for precision = match / return
match_precision=0
for i in range(10):
    imgfile = os.path.join(dbpath, "test_images_" + str(nearest_idx[i+1]) + '.png')
    matched_img = cv2.cvtColor(cv2.imread(imgfile), cv2.COLOR_BGR2RGB)
    axs[i].imshow(matched_img)
    axs[i].set_title(str(i + 1))
    axs[i].set_xticks([])
    axs[i].set_yticks([])

plt.show()
'''









'''
queryfile = '/Users/sebastianpfaff/Documents/Studium/02_TUM/6. Semester/01_TUM Data Innovation Lab/13_Test_briquet/04_SIFT/Train_data/17.jpg'
img = cv2.imread(queryfile)
query_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
transform_img = create_test_image(query_img, 9)
nearest_idx = Find_nearest_index(transform_img, codebook, fv)
position = nearest_idx[17]
print(nearest_idx.index(17))
'''



'''
for path in os.listdir(dbpath):
    k = k+1
    for j in range(1,14):
        
    if k % 1000 ==0:
        print(path)
        print(k)
'''