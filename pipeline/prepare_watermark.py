import cv2
from preprocess_watermarks import preprocess_watermark
import argparse


OUTPUT_PATH = "outputs/"

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str)
    args = parser.parse_args()
    
    image = cv2.imread(args.input_path)
    image = preprocess_watermark(image)

    cv2.imwrite(OUTPUT_PATH/tmp.jpg)
