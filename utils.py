import os

from typing import List
from annotation import Annotation

RAW_IMAGE_PATH = "../data/"

def check_folders_exist(annotations: List[Annotation]):
    folders = list(set([annotation.path.folder_name for annotation in annotations]))
    missing_folders = []
    for folder in folders:
        if not os.path.isdir(os.path.join(RAW_IMAGE_PATH, folder)):
            missing_folders.append(folder)

    if len(missing_folders) > 0:
        print("The following folders are missing:")
        for folder in missing_folders:
            print(folder)
    
    assert len(missing_folders) == 0

def check_images_exist(annotations):
    pass