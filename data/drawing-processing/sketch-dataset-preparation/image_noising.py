import os
import cv2
import scipy
import random
import numpy as np
from tqdm import tqdm

IMAGE_PATH = "../../data/sketch_dataset/A"
NOISY_IMAGE_PATH = "../../data/sketch_dataset/B"
NUM_LINES_LIST = [1, 2, 2, 3, 3, 4, 4, 5]


def apply_noise(image: np.ndarray, max_limit=150):
    noise = 5 + random.randint(50, max_limit) * (np.random.randn(image.shape[0], image.shape[1]) - 0.5)
    noisy_image = np.clip(image + noise, 0, 255)
    
    return noisy_image.astype(np.uint8)

def apply_blur(image: np.ndarray):
    blurry_image = cv2.GaussianBlur(image, (43, 43), cv2.BORDER_DEFAULT)
    
    return blurry_image

def apply_vertical_lines(image: np.ndarray):
    num_lines_list = [1, 2, 2, 3, 3, 4, 4, 5]
    num_lines = random.choice(num_lines_list)
    width, height = image.shape
    line_distance = int(width / num_lines)
    line_thickness = random.randint(3, 8)
    top_distance = random.randint(0, 100)
    bottom_distance = random.randint(0, 100)

    lines_image = np.zeros(image.shape, np.uint8)
    for index in range(0, num_lines):
        distance_to_line = index * line_distance + int(line_distance / 2)
        actual_line_thickness = random.randint(-1, 1) + line_thickness
        
        lines_image = cv2.line(lines_image, (distance_to_line, top_distance), (distance_to_line, image.shape[1] - bottom_distance), (255), actual_line_thickness)
        
    lines_image = scipy.ndimage.rotate(lines_image, random.randint(-10, 10), reshape=False)
    noisy_lines_image = apply_noise(lines_image)
        
    return cv2.bitwise_not(cv2.bitwise_or(cv2.bitwise_not(image), noisy_lines_image))
    
def make_lines_grey(image: np.ndarray):
    threshold_value = random.randint(80, 180)
    threshold = np.full((image.shape[0], image.shape[1]), 170, dtype=int)
    return np.clip(image + threshold, 0, 255), threshold_value

def create_realistic_drawing(image: np.ndarray):
    processed_image = apply_vertical_lines(image)
    processed_image, threshold = make_lines_grey(processed_image)
    processed_image = apply_noise(processed_image, max(int(threshold / 2), 50))
    processed_image = apply_blur(processed_image)  
    
    return processed_image


if __name__=='__main__':
    for folder in os.listdir(IMAGE_PATH):
        print("Processing folder: {}".format(folder))

        folder_path = os.path.join(IMAGE_PATH, folder)
        for image_name in tqdm(os.listdir(folder_path)):
            image_path = os.path.join(folder_path, image_name)
            
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            realistic_image = create_realistic_drawing(image)
            processed_image_path = os.path.join(NOISY_IMAGE_PATH, folder, image_name)
            
            cv2.imwrite(processed_image_path, realistic_image)
            
            
            
