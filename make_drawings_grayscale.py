import os
import cv2
import argparse
from annotation import Label

from constants import PROCESSED_IMAGE_TRAIN_PATH, PROCESSED_IMAGE_VAL_PATH

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str)
    args = parser.parse_args()

    processed_paths = [args.path] if args.path is not None else [PROCESSED_IMAGE_TRAIN_PATH[Label.Drawing], PROCESSED_IMAGE_VAL_PATH[Label.Drawing]] 
    for path in processed_paths:
        for imagepath in os.listdir(path):
            image = cv2.imread(os.path.join(path, imagepath))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(path, imagepath), image)