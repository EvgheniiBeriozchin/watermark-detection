
import cv2 as cv
import numpy as np
from scipy.stats import bernoulli

def create_test_image(img, N):
    # For different type of annotations are done by N
    # N==1: 90 degree rotation
    # N==2: 180 degree rotation
    # N==3: 270 degree rotation
    # N==4: Gaussian blur 5x5 kernel
    # N==5: Gaussian blur 9x9 kernel
    # N==6: Median blur 3
    # N==7: Median blur 5
    # N==8: Keep top half of image
    # N==9: Keep right half of image
    # N==10: Delete circle in the middle
    # N==11: Delete random pixels
    # N==12: Delete random batches
    # N==13: Errode image

    if N == 1:
        # 90 degrees rotation
        res = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
    elif N == 2:
        # 180 degrees rotation
        res = cv.rotate(img, cv.ROTATE_180)
    elif N == 3:
        # 270 degrees rotation
        res = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
    elif N == 4:
        # Gaussian blur Kernel 5,5
        res = cv.GaussianBlur(img, (5, 5), 0)
    elif N == 5:
        # Gaussian blur Kernel 9,9
        res = cv.GaussianBlur(img, (9, 9), 0)
    elif N == 6:
        # Median blur 3
        res = cv.medianBlur(img, 3)
    elif N == 7:
        # Median blur 5
        res = cv.medianBlur(img, 5)
    elif N == 8:
        # Delete lower half
        res = img.copy()
        for i in range(128):
            for j in range(256):
                res[128 + i][j] = (255, 255, 255)
    elif N == 9:
        # Delete left half
        res = img.copy()
        for i in range(256):
            for j in range(128):
                res[i][j] = (255, 255, 255)
    elif N == 10:
        # Delete big circle
        res = img.copy()
        res = cv.circle(res, (128, 128), 50, (255, 255, 255), -1)
        res = cv.circle(res, (128, 128), 50, (255, 255, 255), 5)
    elif N == 11:
        # Delete random pixel
        res = img.copy()
        p = 0.5
        for i in range(256):
            for j in range(256):
                k = bernoulli.rvs(p, size=1)
                if k == 1:
                    res[i][j] = (255, 255, 255)
    elif N == 12:
        # Delete 4x4 square
        p = 0.5
        res = img.copy()
        for i in range(64):
            for j in range(64):
                k = bernoulli.rvs(p, size=1)
                if k == 1:
                    res[(4 * i):(4 * (i + 1)), (4 * j):(4 * (j + 1))] = (255, 255, 255)
    elif N == 13:
        # Using cv2.erode() method
        kernel = np.ones((6, 6), np.uint8)
        res = cv.erode(img, kernel, cv.BORDER_REFLECT)
    else:
        print('Input out of range!')

    return res