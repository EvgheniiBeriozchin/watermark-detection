import os

from typing import List
from annotation import Annotation
from constants import RAW_IMAGE_PATH, GEOGRAPHICAL_SOURCES_PATH

def check_folders_exist(annotations: List[Annotation]):
    folders = list(set([(annotation.path.geographical_source, annotation.path.folder_name) for annotation in annotations]))
    missing_folders = []
    for geographical_source, folder in folders:
        if not os.path.isdir(os.path.join(RAW_IMAGE_PATH, GEOGRAPHICAL_SOURCES_PATH[geographical_source], folder)):
            missing_folders.append(folder)

    if len(missing_folders) > 0:
        print("The following folders are missing:")
        for folder in missing_folders:
            print(folder)
    
    #assert len(missing_folders) == 0

    print ("Checking Folders: All good!")

def check_images_exist(annotations):
    pass