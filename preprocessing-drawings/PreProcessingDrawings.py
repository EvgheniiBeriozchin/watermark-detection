from PreProcessingDrawingsFunctions import make_black_and_white, calculate_black_percentage, is_grayscale
from PreProcessingDrawingsNoRemoval import preprocess_drawing_noremoval
from PreProcessingDrawingsPixel import preprocess_drawing_pixel
from PreProcessingDrawingsWavelets import preprocess_drawing_wavelets
import cv2

remove_vec = [150,400,140,100]
sigma = 10
wname = 'db1'
decNum = 5

def pre_processing_drawing(image,remove_vec,wname,decNum,sigma):

  image_gray = is_grayscale(image)

  bw = make_black_and_white(image_gray)

  result = preprocess_drawing_pixel(bw,remove_vec)
  black_row_percentage, black_col_percentage = calculate_black_percentage(result)

  if (max(black_row_percentage, black_col_percentage)>20):
    result = preprocess_drawing_wavelets(image_gray,wname,decNum,sigma)
    black_row_percentage, black_col_percentage = calculate_black_percentage(result)
    if (max(black_row_percentage, black_col_percentage)>20):
      result = preprocess_drawing_noremoval(bw,[50,200,30,35])
      black_row_percentage, black_col_percentage = calculate_black_percentage(result)
      if (max(black_row_percentage, black_col_percentage)>20):
        result = cv2.bitwise_not(bw)

  return result