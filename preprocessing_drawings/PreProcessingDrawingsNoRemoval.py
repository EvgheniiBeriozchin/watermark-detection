import cv2
from preprocessing_drawings.PreProcessingDrawingsFunctions import make_black_and_white, remove_short_lines, remove_blobs, \
  convert_and_thresholding, is_grayscale
import numpy as np

def preprocess_drawing_noremoval(image, bloob_size):

  img_gray = is_grayscale(image)

  img = cv2.rotate(img_gray, cv2.ROTATE_90_CLOCKWISE)

  img = make_black_and_white(img)

  img = convert_and_thresholding(img)

  img = remove_blobs(img,bloob_size[0])

  result = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

  return result