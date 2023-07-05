import cv2
from preprocess_watermarks import preprocess_watermark

IMAGE_PATH = "../data/dnb/processed/trainA/0027722_1-0.jpg"
OUTPUT_PATH = "outputs/"

if __name__=='__main__':
    image = cv2.imread(IMAGE_PATH)
    image = preprocess_watermark(image)

    cv2.imwrite(OUTPUT_PATH/tmp.jpg)