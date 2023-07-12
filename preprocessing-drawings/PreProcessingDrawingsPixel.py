import cv2
from PreProcessingDrawingsFunctions import make_black_and_white, remove_short_lines, remove_blobs,  \
  find_horizontal_lines,combine_img_hor, convert_and_thresholding, is_grayscale
import numpy as np

def preprocess_drawing_pixel(image, bloob_size):

  img_gray = is_grayscale(image)

  img = cv2.rotate(img_gray, cv2.ROTATE_90_CLOCKWISE)

  img = make_black_and_white(img)

  img = convert_and_thresholding(img)

  im_result = remove_blobs(img,bloob_size[0])

  hor_lines = find_horizontal_lines(im_result)

  hor_lines = remove_blobs(hor_lines,bloob_size[1])

  im_result_hor = remove_short_lines(hor_lines,30)

  img_combined = combine_img_hor(im_result,im_result_hor)

  final_result = remove_blobs(img_combined,bloob_size[2])

  final_result = remove_short_lines(final_result,bloob_size[3])

  result = cv2.rotate(final_result, cv2.ROTATE_90_COUNTERCLOCKWISE)

  return result