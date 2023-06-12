import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def load_target_image(image_path):
    """Read target image and transform to binarized negative of sketch"""
    img = cv2.imread(image_path)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #(thresh, img_bin) = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    #img_bin_inv = cv2.bitwise_not(img_bin)
    print(len(img))

    return img


def load_comparison_watermarks(folder_path):
    """Read comparison images and transform to binarized negative of sketch"""
    images = [cv2.imread(file) for file in glob.glob(folder_path + '/*.png')]
    #images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in images]
    return images


def im_show(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.axis('off')
    plt.imshow(image)
    plt.title('Target Image')
    plt.show()


def get_contour(image, plot_contour = False):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, img_bin) = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    image = cv2.bitwise_not(img_bin)

    ret, thresh1 = cv2.threshold(image, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    if plot_contour == True:
        cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        plt.axis('off')
        plt.imshow(image)
        plt.title('Identifying the Contours')
        plt.show()

    return contours


def compare_image_to_db(img_path, folder_path):
    """Compare contours and return the matching values"""
    target = load_target_image(img_path)
    target_contour = get_contour(target)
    sorted_contours = sorted(target_contour, key=cv2.contourArea, reverse=True)
    #extract the second largest contour which is the shape only
    target_contour = sorted_contours[1]
    db = load_comparison_watermarks(folder_path)

    similar_images = 0

    similarity=[]

    for image in db:
        input_contours = get_contour(image)
        sorted_input = sorted(input_contours, key=cv2.contourArea, reverse=True)
        # extract the second largest contour which is the shape only
        input_contours = sorted_input[1]
        match = cv2.matchShapes(target_contour, input_contours,3,0.0)
        similarity.append([match, image])
        #print(match)

    for simil in similarity:
        if simil[0] < 0.15:
            print('simil:',simil[0])
            cv2.drawContours(target, [target_contour], -1, (0, 255, 0), 3)
            #image = cv2.cvtColor(simil[1], cv2.COLOR_BGR2RGB)
            plt.axis('off')
            plt.imshow(simil[1])
            plt.title('Best matching image')
            plt.show()
            #im_show(simil[1])

            similar_images += 1

    print("Number of similar images:", similar_images)

    return similarity



path = "./Data Shape Comparison/briquet_engraving/briquet_1.png"
folder = "./Data Shape Comparison/briquet_engraving"
img = load_target_image(image_path=path)
im_show(img)

#im_all = load_comparison_watermarks(folder)
db = load_comparison_watermarks(folder)
sim = compare_image_to_db(img_path= path, folder_path=folder)
#print(sim.size)