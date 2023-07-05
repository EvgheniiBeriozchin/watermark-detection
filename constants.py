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
CUT_IMAGE_PATH = {
    Label.Drawing: "../data/dnb/cut/drawings/",
    Label.Watermark: "../data/dnb/cut/watermarks/"
}

TRAIN_PERCENTAGE = 0.95