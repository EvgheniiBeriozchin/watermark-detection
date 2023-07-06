import cv2
from preprocess_watermarks import preprocess_watermark

OUTPUT_PATH = "outputs/"

if __name__=='__main__':
    image = cv2.imread(IMAGE_PATH)
    image = preprocess_watermark(image)
    cv2.imwrite(os.path.join(OUTPUT_PATH, "tmp.jpg"))