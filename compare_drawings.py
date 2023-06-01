import os
import cv2

from argparse import ArgumentParser
from numpy import ndarray
from typing import List
from matplotlib import pyplot as plt

IMAGE_DATABASE_PATH = "../../data/image-database/"

def compare_image_pair(image1: ndarray, image2: ndarray):
    return 0.0

def get_similar_images(target_image: str, *, n_images: int):
    most_similar_images = []
    
    for reference_image_path in os.listdir(IMAGE_DATABASE_PATH):
        reference_image = cv2.imread(os.path.join(IMAGE_DATABASE_PATH, reference_image_path), cv2.IMREAD_GRAYSCALE)
        similarity = compare_image_pair(target_image, reference_image)
        
        if len(most_similar_images) < n_images:
            most_similar_images += [(reference_image, similarity)]
        else:
            most_similar_images[n_images - 1] = (reference_image, similarity)
            
        most_similar_images = sorted(most_similar_images, key=lambda item: item[1], reverse=True)
        
    return most_similar_images
            
def display_similar_images(target_image: ndarray, similar_images: List[ndarray]):
    _, axes = plt.subplots(len(similar_images), 2, figsize=(10, 4 * len(similar_images)))
    
    for index, reference_image in enumerate(similar_images):
        axes[index, 0].imshow(target_image)
        axes[index, 1].imshow(reference_image)
    

if __name__=='__main__':
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-i", "--image", help="image to be compared")
    arguments = argument_parser.parse_args()
    
    target_image = cv2.imread(arguments.image)
    similar_images = get_similar_images(target_image, n_images=5)
    display_similar_images(target_image, [image_pair[0] for image_pair in similar_images])