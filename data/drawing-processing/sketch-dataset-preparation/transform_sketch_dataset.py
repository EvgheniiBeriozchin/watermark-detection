import os
import shutil
import random

RAW_IMAGE_PATH = "../../data/sketch_dataset_raw/"
IMAGE_PATH = "../../data/sketch_dataset/A"

val_percentage = 0.15

if __name__=='__main__':
    index = 1
    for folder in os.listdir(RAW_IMAGE_PATH):
        folder_path = os.path.join(RAW_IMAGE_PATH, folder)
        if not os.path.isdir(folder_path):
            continue
        
        for image in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image)
            
            moved_folder = os.path.join(IMAGE_PATH, random.choices(["val", "train"], weights=[1, int(100 * val_percentage) - 1])[0])
            shutil.move(image_path, os.path.join(moved_folder, "{}.png".format(index)))
            index += 1
