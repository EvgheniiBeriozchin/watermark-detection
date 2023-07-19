from typing import List
from annotation import Annotation
from load_annotations import load_raw_annotations, parse_raw_annotations
from preprocess_images import preprocess_images
from utils import check_folders_exist

TEST_IMAGE_LIST_PATH = "benchmarking/TestSetLabels"
def remove_test_images(annotations: List[Annotation]):
    with open(TEST_IMAGE_LIST_PATH, "r") as f:
        ignored_image_lines = f.readlines()[1:]
        ignored_image_paths = [ignored_image_line.split(",")[0].split("/") for ignored_image_line in ignored_image_lines]
        annotations = list(filter(lambda annotation: (annotation.path.folder_name, annotation.path.file_name) 
                                                not in ignored_image_paths, annotations))
        
        return annotations

if __name__ == '__main__':
    raw_annotations = load_raw_annotations()
    annotations = parse_raw_annotations(raw_annotations)
    annotations = remove_test_images(annotations)
    
    check_folders_exist(annotations)
    preprocess_images(annotations)