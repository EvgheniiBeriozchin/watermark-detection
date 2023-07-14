GENERATED_DRAWING_PATH = "outputs/tmp.jpg"
ALL_DRAWINGS_PATH = "../data/dnb/db/"
OUTPUT_PATH = "outputs/"

import cv2
import os
import shutil
from image_comparison.annoy_extract_features import build_annoy_index
from image_comparison.annoy_lookup import get_nns_spotify_annoy

if __name__=="__main__":
    annoy_index, image_names = build_annoy_index(ALL_DRAWINGS_PATH)
    _, nearest_neighbors = get_nns_spotify_annoy(GENERATED_DRAWING_PATH, annoy_index, image_names)
    for i, neighbor in enumerate(nearest_neighbors[:10]):
        shutil.copy(os.path.join(ALL_DRAWINGS_PATH, neighbor), os.path.join(OUTPUT_PATH, "{}.jpg".format(neighbor)))