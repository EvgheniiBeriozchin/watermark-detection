import cv2
from numpy import ndarray

def make_black_and_white(image: ndarray):
    result = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)

    return result

def preprocess_drawing(image: ndarray):
    image = make_black_and_white(image)
    
    return image