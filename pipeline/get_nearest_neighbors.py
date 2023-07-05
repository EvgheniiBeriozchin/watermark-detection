GENERATED_DRAWING_PATH = "../results/dnb-model-v1.1/dnb-model-v1.1/test_latest/images/0001221_1-01-0_real_B.png"
ALL_DRAWINGS_PATH = "../results/dnb-model-v1.1/dnb-model-v1.1/test_latest/images"
OUTPUT_PATH = "outputs/"

from image_comparison.annoy_extract_features import build_annoy_index
from image_comparison.annoy_lookup import get_nns_spotify_annoy

if __name__=="__main__":
    annoy_index, image_names = build_annoy_index(ALL_DRAWINGS_PATH)
    _, nearest_neighbors = get_nns_spotify_annoy(GENERATED_DRAWING_PATH, annoy_index, image_names)

    for i, neighbor in enumerate(nearest_neighbors):
        cv2.imwrite(os.path.join(OUTPUT_PATH, "output{}.jpg".format(i)), neighbor)