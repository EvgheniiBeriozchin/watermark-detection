from load_annotations import load_raw_annotations, parse_raw_annotations
from preprocess_images import preprocess_images
from utils import check_folders_exist


if __name__ == '__main__':
    raw_annotations = load_raw_annotations()
    annotations = parse_raw_annotations(raw_annotations)
    
    check_folders_exist(annotations)
    preprocess_images(annotations)