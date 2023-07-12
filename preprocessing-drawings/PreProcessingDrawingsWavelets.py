import cv2
import numpy as np
from PreProcessingDrawingsFunctions import xRemoveStripesVertical, remove_short_lines, is_grayscale

def preprocess_drawing_wavelets(image,wname,decNum,sigma):

  img_gray = is_grayscale(image)

  img = xRemoveStripesVertical(img_gray, wname, decNum, sigma)

  kernel = np.ones((3, 3), np.uint8)
  img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)
  img = cv2.fastNlMeansDenoising(img, None, 20, 20, 7)
  img = cv2.dilate(img, kernel, iterations=1)
  kernel = np.ones((5, 5), np.uint8)
  img = cv2.erode(img, kernel, iterations=1)
  ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
  img = cv2.bitwise_not(img)
  result = remove_short_lines(img, 50)


  return result