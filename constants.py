from annotation import Label


RAW_IMAGE_PATH = "../data/dnb/raw/"
PROCESSED_IMAGE_TRAIN_PATH = {
    Label.Drawing: "../data/dnb/processed/trainB",
    Label.Watermark: "../data/dnb/processed/trainA",
}
PROCESSED_IMAGE_VAL_PATH = {
    Label.Drawing: "../data/dnb/processed/testB",
    Label.Watermark: "../data/dnb/processed/testA",
}

TRAIN_PERCENTAGE = 0.95
IMAGE_SIZE = (256, 256)
NOISE_WINDOW = 12
MEDIAN_FILTER_SIZE = 7