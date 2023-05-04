import cv2
import numpy as np
import matplotlib.pyplot as plt

def im_show(image, name = None):
    plt.axis('off')
    plt.imshow(image)
    plt.title(name)
    plt.show()

path = "./Test images/0006473_2.png"
#img = load_target_image(image_path=path)
#im_show(img)
s = 110
img = cv2.imread(path)
mask = cv2.threshold(img, s, 255, cv2.THRESH_BINARY_INV)[1][:,:,0]
(thresh, target_gray) = cv2.threshold(img, s, 255, cv2.THRESH_BINARY)
invert = cv2.bitwise_not(target_gray)#[1]#[:,:,0]
dst = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)


im_show(img, name="Image")
im_show(target_gray, name="Mask")
im_show(dst, name="Processed")