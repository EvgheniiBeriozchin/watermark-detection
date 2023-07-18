import cv2
from numpy import ndarray
from preprocessing_drawings.PreProcessingDrawings import pre_processing_drawing

def make_black_and_white(image: ndarray):
    result = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)

    return result

def preprocess_drawing(image: ndarray, use_classical_preprocessing=False):
    # image = make_black_and_white(image)
    if use_classical_preprocessing:
        image = pre_processing_drawing(image)

    return image