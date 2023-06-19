from annotation import Label, GeographicalSource


RAW_IMAGE_PATH = "../data/dnb/raw/"

GEOGRAPHICAL_SOURCES_PATH = {
    GeographicalSource.Thuringen: "WZ_II_Thueringen",
    GeographicalSource.Sachsen: "WZ_II_Sachsen",
}
PROCESSED_IMAGE_TRAIN_PATH = {
    Label.Drawing: "../data/dnb/processed/trainB",
    Label.Watermark: "../data/dnb/processed/trainA",
}
PROCESSED_IMAGE_VAL_PATH = {
    Label.Drawing: "../data/dnb/processed/testB",
    Label.Watermark: "../data/dnb/processed/testA",
}

TRAIN_PERCENTAGE = 0.95