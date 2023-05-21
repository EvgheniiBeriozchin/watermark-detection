import os
from typing import List
import cv2
from math import floor, ceil

from annotation import Annotation, Label
from preprocess_drawings import preprocess_drawing
from preprocess_watermarks import preprocess_watermarks

RAW_IMAGE_PATH = "../data/"
PROCESSED_IMAGE_PATH = "../processed_data/"

def load_and_preprocess_raw_image(annotation: Annotation):
    image = cv2.imread(os.path.join(RAW_IMAGE_PATH, annotation.path.folder_name))

    processed_images = []
    for bounding_box in annotation.bounding_boxes:
        start_row = floor(bounding_box.y)
        end_row = ceil(bounding_box.y + bounding_box.height)

        start_column = floor(bounding_box.x)
        end_column = ceil(bounding_box.x + bounding_box.width)

        cropped_image = image[start_row:end_row, start_column:end_column]

        if bounding_box.label == Label.Drawing:
            processed_images.append(preprocess_drawing(cropped_image))

        elif bounding_box.label == Label.Watermark:
            processed_images.append(preprocess_watermarks(cropped_image))

    return processed_images


def preprocess_images(annotations: List[Annotation]):
    for annotation in annotations:
        processed_images = load_and_preprocess_raw_image(annotation)

        for i, processed_image in enumerate(processed_images):
            if not os.path.isdir(annotation.path.folder_name):
                os.mkdir(annotation.path.folder_name)
            
            file_name = annotation.path.file_name
            if len(processed_images) > 1:
                [name, extension] = file_name.split(".")
                file_name = name + "-{}.".format(i) + extension

            image_path = os.path.join(annotation.path.folder_name, file_name)
            
            cv2.imwrite(image_path, processed_image)

