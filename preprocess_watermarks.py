from numpy import ndarray
import cv2
import numpy as np
from matplotlib import pyplot as plt



def strech_contrast(image):
    """Strech contrast of image"""
    min_val = np.min(image)
    max_val = np.max(image)
    stretched_image = 255 * ((image - min_val) / (max_val - min_val))
    stretched_image = stretched_image.astype(np.uint8)
    image = stretched_image
    return image


def remove_ink(image):
    """Remove ink and dark colors on images"""
    if len(image.shape) < 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    s = 100
    mask = cv2.threshold(image, s, 255, cv2.THRESH_BINARY_INV)[1][:, :, 0]
    (thresh, target_gray) = cv2.threshold(image, s, 255, cv2.THRESH_BINARY)
    invert = cv2.bitwise_not(target_gray)  # [1]#[:,:,0]
    dst = cv2.inpaint(image, mask, 7, cv2.INPAINT_NS)
    return dst

def adaptive_thresh(image):
    """Remove ink and dark colors on images"""
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.medianBlur(image,5)
    th3 = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return th3


def remove_darker_foreground(image, structuring_element_size = 3, iterations = 6):
    """Remove darker parts of the image using dilate and erode"""
    structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT,
                                                    (structuring_element_size, structuring_element_size))
    dilated_image = cv2.dilate(image, structuring_element, iterations=iterations)
    eroded_image = cv2.erode(dilated_image, structuring_element, iterations=iterations)
    removed_foreground = cv2.absdiff(image, eroded_image)
    removed_foreground = cv2.bitwise_not(removed_foreground)
    return removed_foreground, dilated_image, eroded_image


def top_minus_back(image):
    """Remove noisy background from image"""
    k1 = 20
    filterSize = (k1, k1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, filterSize)

    if len(image.shape) > 2:
        input_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    tophat_img = cv2.morphologyEx(input_image, cv2.MORPH_TOPHAT, kernel)
    k2 = 6
    filterSize2 = (k2, k2)
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, filterSize2)
    blackhat_img = cv2.morphologyEx(input_image, cv2.MORPH_BLACKHAT, kernel2)
    filtered = cv2.absdiff(tophat_img, blackhat_img)
    return filtered


def remove_nonuniform_background(image, structuring_element_size=20): #25
    structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT,
                                                    (structuring_element_size, structuring_element_size))
    background = cv2.morphologyEx(image, cv2.MORPH_OPEN, structuring_element)
    top_hat = cv2.subtract(image, background)
    return top_hat


def lighten_image(image):
    if len(image.shape) > 2:
        input_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    alpha = 5 #5  # Increase this value to make the image lighter
    beta = 10 #10  # Leave this value as 0 for now
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    _, thresholded_image = cv2.threshold(adjusted_image, 155, 255, cv2.THRESH_BINARY)
    return thresholded_image, adjusted_image


def wrap_image(image, n = 1):
    if len(image.shape) > 2:
        input_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Extract the rows to be moved to the bottom
    top_rows = image[:n, :]

    # Remove the extracted rows from the image
    removed_rows_image = image[n:, :]

    modified_image = np.concatenate((removed_rows_image, top_rows), axis=0)
    return modified_image

def im_show(image, name=None):
    if len(image.shape) > 2:
        input_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.axis('off')
    plt.imshow(image, cmap='gray')
    plt.title(name)
    plt.show()

path_imwrite = "/Users/pauli/Documents/Studium/Master/4_Semester/TUM_DI_Lab/Final Report/Images/"


def preprocess_watermark(image: ndarray):
    image = strech_contrast(image)
    image = remove_ink(image)
    image = top_minus_back(image)
    image, adjusted = lighten_image(image)
    image_store = image
    image, eroded, dilated = remove_darker_foreground(adjusted)
    image = remove_nonuniform_background(image)
    im_show(image, name="Remove_background")
    image = wrap_image(image, n=0)
    alpha = 0.7
    image = cv2.addWeighted(image, alpha, image_store, 1-alpha, 0.0)
    image = cv2.GaussianBlur(image, (5, 5), 0)

    return image





