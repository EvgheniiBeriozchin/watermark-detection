import os
import json
from typing import List

from annotation import Annotation, BoundingBox, Flag, GeographicalSource, Label, Path

BATCHES_PATH = "./data-annotation/"
BATCHES_FOLDERS_START = "batch-"
SACHSEN_FOLDER_NAME = "WZ_II_Sachsen"


def load_raw_annotations():
    annotations = []
    for folder in os.listdir(BATCHES_PATH):
        if (folder.startswith(BATCHES_FOLDERS_START)):
            for filename in os.listdir(os.path.join(BATCHES_PATH, folder)):
                if (not filename.endswith(".json")):
                    continue
                    
                with open(os.path.join(BATCHES_PATH, folder, filename), "r") as f:
                    annotation_batch = json.load(f)
                    annotations += annotation_batch

    return annotations

def parse_raw_annotations(raw_annotations):
    annotations: List[Annotation] = []
    for index, raw_annotation in enumerate(raw_annotations):
        split_path = raw_annotation["data"]["image"].split("/")[-3:]
        path = Path(
            geographical_source=GeographicalSource.Thuringen 
            if split_path[0] != SACHSEN_FOLDER_NAME 
            else GeographicalSource.Sachsen,
            folder_name=split_path[1],
            file_name=split_path[2]
            )
        
        if len(raw_annotation["annotations"]) > 1:
            raise Exception("The file with id {} has multiple annotations".format(raw_annotation["id"]))
        
        annotation_results = raw_annotation["annotations"][0]["result"]
        source_unique_id = raw_annotation["annotations"][0]["unique_id"]
        flags: List[Flag] = []
        bounding_boxes: List[BoundingBox] = []

        for result in annotation_results:
            if result["type"] == "choices":
                flags += result["value"]["choices"]

            elif result["type"] == "rectanglelabels":
                raw_bounding_box = result["value"]
                if len(raw_bounding_box["rectanglelabels"]) > 1:
                    raise Exception("The annotation for file with id {} has multiple labels".format(raw_annotation["id"]))

                bounding_boxes.append(BoundingBox(
                                        x=raw_bounding_box["x"],
                                        y=raw_bounding_box["y"],
                                        width=raw_bounding_box["width"],
                                        height=raw_bounding_box["height"],
                                        rotation=raw_bounding_box["rotation"],
                                        label=Label[raw_bounding_box["rectanglelabels"][0]],
                                        )
                                    )


        annotation = Annotation(id=index, 
                                path=path, 
                                source_unique_id=source_unique_id,
                                bounding_boxes=bounding_boxes,
                                flags=flags,
                                )
        
        annotations.append(annotation)

    return annotations

if __name__=='__main__':
    raw_annotations = load_raw_annotations()
    annotations = parse_raw_annotations(raw_annotations)
    print(annotations[0])