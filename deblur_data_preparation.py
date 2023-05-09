import os
import shutil
from PIL import Image

DATA_SOURCE_PATH = "/mnt/c/Users/evghe/LRZ Sync+Share/Watermarks/XiShen/B_cross_domain_plus/"
DATA_TARGET_PATH = "../data/xishen-prepared/"


def prepare_xishen_data():
    for split in os.listdir(DATA_SOURCE_PATH):
        print("Current split: {}".format(split))
        current_path = DATA_SOURCE_PATH + split + "/"
        os.mkdir(DATA_TARGET_PATH + split + "/A/")
        os.mkdir(DATA_TARGET_PATH + split + "/B/")
        for class_folder in os.listdir(current_path):
            drawing_path = current_path + class_folder + "/0.png"
            image_path = current_path + class_folder + "/1.jpg"
            if os.path.isfile(drawing_path) and os.path.isfile(image_path):
                shutil.copyfile(drawing_path, DATA_TARGET_PATH + split + "/B/{}.png".format(class_folder))
                im = Image.open(image_path)
                im.save(DATA_TARGET_PATH + split + "/A/{}.png".format(class_folder))

if __name__=='__main__':
    prepare_xishen_data()