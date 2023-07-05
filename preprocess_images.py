import os
from typing import List
from constants import PROCESSED_IMAGE_TRAIN_PATH, PROCESSED_IMAGE_VAL_PATH, RAW_IMAGE_PATH, TRAIN_PERCENTAGE, CUT_IMAGE_PATH
import cv2
from math import floor, ceil
from random import choices

from annotation import Annotation, Label
from preprocess_drawings import preprocess_drawing
from preprocess_watermarks import preprocess_watermark
from db.insert_utils import insert_bounding_box_to_db, insert_cut_image_to_db, insert_processed_image_to_db


def load_and_preprocess_raw_image(cursor, annotation: Annotation):
    image = cv2.imread(os.path.join(RAW_IMAGE_PATH, annotation.path.folder_name, annotation.path.file_name), 
                       cv2.IMREAD_GRAYSCALE)

    processed_images = {}
    processed_images[Label.Drawing] = []
    processed_images[Label.Watermark] = []

    if image is None:
        return processed_images

    for bounding_box in annotation.bounding_boxes:
        bounding_box_id = insert_bounding_box_to_db(cursor, annotation, bounding_box)
        start_row = floor(bounding_box.y * 0.01 * image.shape[0])
        end_row = ceil((bounding_box.y + bounding_box.height) * image.shape[0] * 0.01)

        start_column = floor(bounding_box.x * image.shape[1] * 0.01)
        end_column = ceil((bounding_box.x + bounding_box.width) * image.shape[1] * 0.01)

        cropped_image = image[start_row:end_row, start_column:end_column]
        
        if bounding_box.label == Label.Drawing:
            processed_images[Label.Drawing].append((bounding_box_id, cropped_image, preprocess_drawing(cropped_image)))
            
        elif bounding_box.label == Label.Watermark:
            processed_images[Label.Watermark].append((bounding_box_id, cropped_image, preprocess_watermark(cropped_image)))
    
    return processed_images


def preprocess_images(cursor, annotations: List[Annotation]):
    data_splitting_folders = [PROCESSED_IMAGE_TRAIN_PATH, PROCESSED_IMAGE_VAL_PATH]
    data_splitting_weights = [TRAIN_PERCENTAGE, 1.0 - TRAIN_PERCENTAGE]
    print("Processing images for {} annotations".format(len(annotations)))

    for i, annotation in enumerate(annotations):
        processed_images = load_and_preprocess_raw_image(annotation)

        for label in [Label.Drawing, Label.Watermark]:
            for j, bounding_box_id, cropped_image, processed_image in enumerate(processed_images[label]):
                cropped_folder_path = CUT_IMAGE_PATH[label]
                processed_folder_path = choices(data_splitting_folders, data_splitting_weights)[0][label]

                if not os.path.isdir(cropped_folder_path):
                    os.mkdir(cropped_folder_path)

                if not os.path.isdir(processed_folder_path):
                    os.mkdir(processed_folder_path)
                
                file_name = annotation.path.file_name
                if len(processed_images) > 1:
                    [name, extension] = file_name.split(".")
                    file_name = name + "-{}.".format(j) + extension

                cropped_image_path = os.path.join(cropped_folder_path, file_name)
                processed_image_path = os.path.join(processed_folder_path, file_name)

                cv2.imwrite(cropped_image_path, cropped_image)
                cv2.imwrite(processed_image_path, processed_image)

                cropped_image_id = insert_cut_image_to_db(cursor, cropped_image_path, bounding_box_id)
                insert_processed_image_to_db(cursor, processed_image_path, cropped_image_id)

        if i > 0 and i % 50 == 0:
            print("Processed {} annotations".format(i))
