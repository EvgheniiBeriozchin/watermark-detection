
import cv2
import numpy as np
import pywt


def make_black_and_white(image):
    result = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)

    return result

def erode_and_dilate(image):

  img = image.astype('uint8')
  kernel = np.ones((3, 3), np.uint8)
  img = cv2.erode(img, kernel)
  kernel = np.ones((5, 5), np.uint8)
  result = cv2.dilate(img, kernel, iterations=1)

  return result

def remove_blobs(image, min_size):

  nb_blobs, im_with_separated_blobs, stats, _ = cv2.connectedComponentsWithStats(image)
  sizes = stats[:, -1]
  sizes = sizes[1:]
  nb_blobs -= 1

  img_result = np.zeros_like(im_with_separated_blobs)

  for blob in range(nb_blobs):
      if sizes[blob] >= min_size:
          img_result[im_with_separated_blobs == blob + 1] = 255

  result = img_result.astype('uint8')
  return result


def remove_short_lines(image, min_length=None):

    lines_contour = image.astype('uint8')

    if min_length is None:
        h, w = lines_contour.shape
        min_length = (2*w*0.3)

    lines_contour = image.astype('uint8')

    contours, hierarchy = cv2.findContours(lines_contour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for i, c in enumerate(contours):
        length_tresh = min_length
        length = cv2.arcLength(c,True)
        if length < length_tresh:
            cv2.drawContours(lines_contour, contours, i, 0, cv2.FILLED)

    result = lines_contour

    return result

def find_horizontal_lines(image):

    horizontal = np.copy(image)

    cols = horizontal.shape[1]

    horizontal_size = cols // 20

    if horizontal_size <= 0:
        horizontal_size = 1

    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)

    horizontal = cv2.bitwise_not(horizontal)

    edges = cv2.adaptiveThreshold(horizontal, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, -2)
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel)
    smooth = np.copy(horizontal)
    smooth = cv2.blur(smooth, (2, 2))

    (rows, cols) = np.where(edges != 0)
    horizontal[rows, cols] = smooth[rows, cols]
    result = cv2.bitwise_not(horizontal)

    return result

def combine_img_hor(image,img_hor):
  im_combined = abs(image - img_hor)
  result = cv2.normalize(src=im_combined, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
  return result

def convert_and_thresholding(image):
  img = cv2.convertScaleAbs(image)
  gray = cv2.bitwise_not(img)
  bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
  ret,result = cv2.threshold(bw,10,255,cv2.THRESH_BINARY)
  return result

def xRemoveStripesVertical(image, wname, decNum, sigma):

  coeffs = pywt.wavedec2(image, wavelet=wname, level=decNum)
  cA = coeffs[0]
  print(cA.shape)
  a = [(cA)]
  for i in range (1,decNum+1):

      cH = coeffs[i][0]
      cV = coeffs[i][1]

      fCv = np.fft.fftshift(np.fft.fft(cV), axes=None)
      my, mx = fCv.shape
      damp = 1 - np.exp(-(np.arange(-my // 2, my // 2) ** 2) / (2 * sigma ** 2))
      fCv = fCv * np.tile(damp[:, np.newaxis], (1, mx))
      CV_new = np.fft.ifft(np.fft.ifftshift(fCv))

      cD = coeffs[i][2]
      a.append((cH,CV_new,cD))


  modified_coeffs =  tuple(a)
  nima = pywt.waverec2(modified_coeffs, wname)
  img_real_part = nima.real
  result = np.uint8(img_real_part)
  return result

def calculate_black_percentage(image):
    rows, cols = image.shape

    black_rows = 0
    for row in range(rows):
        if all(image[row] == 0):
            black_rows += 1

    black_cols = 0
    for col in range(cols):
        if all(image[:, col] == 0):
            black_cols += 1

    black_row_percentage = (black_rows / rows) * 100
    black_col_percentage = (black_cols / cols) * 100

    return black_row_percentage, black_col_percentage

def is_grayscale(image):
    # Check if the image has only one color channel
    if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):
        return image

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image