import os
import cv2
import random
import numpy as np

IMAGE_PATH = "../../data/sketch_dataset/A"
NOISY_IMAGE_PATH = "../../data/sketch_dataset/B"
NUM_LINES_LIST = [1, 2, 2, 3, 3, 4, 4, 5]


def apply_noise(image: np.ndarray):
    noise = 5 + random.randint(50, 150) * (np.random.randn(image.shape[0], image.shape[1]) - 0.5)
    noisy_image = np.clip(image + noise, 0, 255)
    
    return noisy_image.astype(np.uint8)

def apply_vertical_lines(image: np.ndarray):
    num_lines = random.choice(NUM_LINES_LIST)
    width, height = image.shape
    line_distance = int(width / num_lines)
    line_thickness = random.randint(3, 8)

    lines_image = np.zeros(image.shape, np.uint8)
    for index in range(0, num_lines):
        distance_to_line = index * line_distance + int(line_distance / 2)
        actual_line_thickness = random.randint(-1, 1) + line_thickness

        lines_image = cv2.line(lines_image, (distance_to_line,50), (distance_to_line, 1000), (255), actual_line_thickness)
        
        
    return cv2.bitwise_not(cv2.bitwise_or(cv2.bitwise_not(image), lines_image))
    
def create_realistic_drawing(image: np.ndarray):
    noisy_image = apply_noise(image)
    realistic_image = apply_vertical_lines(noisy_image)
    
    return realistic_image


if __name__=='__main__':
    for folder in os.listdir(IMAGE_PATH):
        folder_path = os.path.join(IMAGE_PATH, folder)
        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)
            
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            realistic_image = create_realistic_drawing(image)
            processed_image_path = os.path.join(NOISY_IMAGE_PATH, folder, image_name)
            
            cv2.imwrite(processed_image_path, realistic_image)
            
            
            
