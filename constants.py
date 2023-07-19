from annotation import Label, GeographicalSource


RAW_IMAGE_PATH = "../Data_Labeling/TestsetAnnotated/"

GEOGRAPHICAL_SOURCES_PATH = {
    GeographicalSource.Thuringen: "WZ_II_Thueringen",
    GeographicalSource.Sachsen: "WZ_II_Sachsen",
}
PROCESSED_IMAGE_TRAIN_PATH = {
    Label.Drawing: "../Data_Labeling/TestsetAnnotated/processed/trainB",
    Label.Watermark: "../Data_Labeling/TestsetAnnotated/processed/trainA",
}
PROCESSED_IMAGE_VAL_PATH = {
    Label.Drawing: "../Data_Labeling/TestsetAnnotated/processed/testB",
    Label.Watermark: "../Data_Labeling/TestsetAnnotated/processed/testA",
}

TRAIN_PERCENTAGE = 0.95