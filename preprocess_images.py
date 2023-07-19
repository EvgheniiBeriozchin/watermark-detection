import os
from typing import List
from constants import PROCESSED_IMAGE_TRAIN_PATH, PROCESSED_IMAGE_VAL_PATH, GEOGRAPHICAL_SOURCES_PATH, RAW_IMAGE_PATH, TRAIN_PERCENTAGE, IMAGE_SIZE, NOISE_WINDOW, MEDIAN_FILTER_SIZE
import cv2
import numpy as np
from math import floor, ceil
from random import choices
from scipy.ndimage import median_filter 

from annotation import Annotation, Label
from preprocess_drawings import preprocess_drawing
from preprocess_watermarks import preprocess_watermark

def resize_image(image: np.ndarray):
    median = np.median(image)
    vertical_border = 0
    horizontal_border = 0
    size_ratio = IMAGE_SIZE[0] / IMAGE_SIZE[1]

    if size_ratio >= (image.shape[0] / image.shape[1]):
        vertical_border = int((size_ratio * image.shape[1] - image.shape[0]) / 2)
    else:
        horizontal_border = int((size_ratio * image.shape[0] - image.shape[1]) / 2)
    
    image = cv2.copyMakeBorder(image, vertical_border, vertical_border, horizontal_border, horizontal_border, cv2.BORDER_CONSTANT, None)
    image = cv2.resize(image, IMAGE_SIZE)

    noise = median + NOISE_WINDOW * (np.random.randn(image.shape[0], image.shape[1]) - 0.5)
    noise = np.clip(noise, 0, 255)
    noise = median_filter(noise, size = MEDIAN_FILTER_SIZE)
    image = np.where(image == 0, noise, image)

    return image


def load_and_preprocess_raw_image(annotation: Annotation):
    image = cv2.imread(os.path.join(RAW_IMAGE_PATH, GEOGRAPHICAL_SOURCES_PATH[annotation.path.geographical_source], 
                                    annotation.path.folder_name, annotation.path.file_name), 
                       cv2.IMREAD_GRAYSCALE)

    processed_images = {}
    processed_images[Label.Drawing] = []
    processed_images[Label.Watermark] = []

    if image is None:
        return processed_images

    for bounding_box in annotation.bounding_boxes:
        start_row = floor(bounding_box.y * 0.01 * image.shape[0])
        end_row = ceil((bounding_box.y + bounding_box.height) * image.shape[0] * 0.01)

        start_column = floor(bounding_box.x * image.shape[1] * 0.01)
        end_column = ceil((bounding_box.x + bounding_box.width) * image.shape[1] * 0.01)

        cropped_image = image[start_row:end_row, start_column:end_column]
        resized_image = resize_image(cropped_image)
        
        if bounding_box.label == Label.Drawing:
            processed_images[Label.Drawing].append(preprocess_drawing(resized_image))
            
        elif bounding_box.label == Label.Watermark:
            processed_images[Label.Watermark].append(preprocess_watermark(resized_image))
    
    return processed_images


def preprocess_images(annotations: List[Annotation]):
    data_splitting_folders = [PROCESSED_IMAGE_TRAIN_PATH, PROCESSED_IMAGE_VAL_PATH]
    data_splitting_weights = [TRAIN_PERCENTAGE, 1.0 - TRAIN_PERCENTAGE]
    print("Processing images for {} annotations".format(len(annotations)))

    for i, annotation in enumerate(annotations):
        processed_images = load_and_preprocess_raw_image(annotation)

        for label in [Label.Drawing, Label.Watermark]:
            for i, processed_image in enumerate(processed_images[label]):

                folder_path = choices(data_splitting_folders, data_splitting_weights)[0][label]
                if not os.path.isdir(folder_path):
                    os.mkdir(folder_path)
                
                file_name = annotation.path.file_name
                if len(processed_images) > 1:
                    [name, extension] = file_name.split(".")
                    file_name = name + "-{}.".format(i) + extension

                image_path = os.path.join(folder_path, file_name)

                cv2.imwrite(image_path, processed_image)

        if i > 0 and i % 50 == 0:
            print("Processed {} annotations".format(i))
