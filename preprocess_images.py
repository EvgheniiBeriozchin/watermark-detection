import os
from typing import List
from constants import PROCESSED_IMAGE_PATH, RAW_IMAGE_PATH
import cv2
from math import floor, ceil

from annotation import Annotation, Label
from preprocess_drawings import preprocess_drawing
from preprocess_watermarks import preprocess_watermark


def load_and_preprocess_raw_image(annotation: Annotation):
    image = cv2.imread(os.path.join(RAW_IMAGE_PATH, annotation.path.folder_name, annotation.path.file_name), 
                       cv2.IMREAD_GRAYSCALE)

    processed_images = {}
    processed_images[Label.Drawing] = []
    processed_images[Label.Watermark] = []

    for bounding_box in annotation.bounding_boxes:
        start_row = floor(bounding_box.y * 0.01 * image.shape[0])
        end_row = ceil((bounding_box.y + bounding_box.height) * image.shape[0] * 0.01)

        start_column = floor(bounding_box.x * image.shape[1] * 0.01)
        end_column = ceil((bounding_box.x + bounding_box.width) * image.shape[1] * 0.01)

        cropped_image = image[start_row:end_row, start_column:end_column]
        
        if bounding_box.label == Label.Drawing:
            processed_images[Label.Drawing].append(preprocess_drawing(cropped_image))
            
        elif bounding_box.label == Label.Watermark:
            processed_images[Label.Watermark].append(preprocess_watermark(cropped_image))
    
    return processed_images


def preprocess_images(annotations: List[Annotation]):
    
    print("Processing images for {} annotations".format(len(annotations)))

    for i, annotation in enumerate(annotations):
        processed_images = load_and_preprocess_raw_image(annotation)

        for label in [Label.Drawing, Label.Watermark]:
            for i, processed_image in enumerate(processed_images[label]):
                folder_path = os.path.join(PROCESSED_IMAGE_PATH[label], annotation.path.folder_name)
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
