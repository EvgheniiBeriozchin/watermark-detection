

# Import packages
import keras.utils as image
import numpy as np
from keras.applications.imagenet_utils import decode_predictions, preprocess_input


def load_image(path,model):
    img = image.load_img(path, target_size=model.input_shape[1:3])
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return img, x