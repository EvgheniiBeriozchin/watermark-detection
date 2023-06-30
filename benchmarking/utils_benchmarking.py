import pandas as pd
import numpy as np
import cv2
import glob

def load_test_watermarks(folder_path):
    """Read comparison images and transform to binarized negative of sketch"""
    images = [cv2.imread(file) for file in glob.glob(folder_path + '/*.png')]
    #images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in images]
    return images

def get_accuracy(model, path_test_watermarks, path_csv, path_embeddings, n_nearest_neighbors = 10):
    model.eval()
    testset = pd.read_csv(path_csv)
    embeddings = np.load(path_embeddings)

    images = load_test_watermarks(path_test_watermarks)

    matching_drawing = np.zeros(len(images))

    for i, image in enumerate(images):
        output = model(image) # Adjust to model input requirements
        get_embeddings = embeddings_funtion(output)
        


