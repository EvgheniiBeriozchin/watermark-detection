import os
import cv2
from annotation import Label

from constants import PROCESSED_IMAGE_TRAIN_PATH, PROCESSED_IMAGE_VAL_PATH

if __name__=='__main__':
    for imagepath in os.listdir(PROCESSED_IMAGE_TRAIN_PATH[Label.Drawing]):
        image = cv2.imread(os.path.join(PROCESSED_IMAGE_TRAIN_PATH[Label.Drawing], imagepath))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(PROCESSED_IMAGE_TRAIN_PATH[Label.Drawing], imagepath), image)

    for imagepath in os.listdir(PROCESSED_IMAGE_VAL_PATH[Label.Drawing]):
        image = cv2.imread(os.path.join(PROCESSED_IMAGE_VAL_PATH[Label.Drawing], imagepath))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(PROCESSED_IMAGE_VAL_PATH[Label.Drawing], imagepath), image)