import cv2
from preprocess_watermarks import preprocess_watermark
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_path", type=str)
args = parser.parse_args()

IMAGE_PATH = args.input_path
OUTPUT_PATH = "outputs/"

if __name__=='__main__':
    image = cv2.imread(IMAGE_PATH)
    image = preprocess_watermark(image)

    cv2.imwrite(OUTPUT_PATH/tmp.jpg)