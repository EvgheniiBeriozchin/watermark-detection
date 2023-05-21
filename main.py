from load_annotations import load_raw_annotations, parse_raw_annotations
from preprocess_images import preprocess_images


if __name__ == '__main__':
    raw_annotations = load_raw_annotations()
    annotations = parse_raw_annotations(raw_annotations)

    preprocess_images(annotations)