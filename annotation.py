from dataclasses import dataclass
from enum import Enum
from typing import List

class GeographicalSource(Enum):
    Thuringen = 0,
    Sachsen = 1

class Flag(Enum):
    TOW = "TOW",
    MII = "MII",
    SLBB = "SLBB",
    TII = "TII",
    IW = "IW",
    RBB = "RBB",
    MBB = "MBB",
    NBB = "NBB",
    OMBB = "OMBB"

class Label(Enum):
    Watermark = "Watermark",
    Drawing = "Drawing"

@dataclass
class Path:
    geographical_source: GeographicalSource
    folder_name: str
    file_name: str

@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float
    rotation: float
    label: Label


@dataclass
class Annotation:
    id: int
    path: Path
    bounding_boxes: List[BoundingBox]
    flags: List[Flag]
    source_unique_id: str


@dataclass
class SingleAnnotation:
    id: int
    annotation_id: int
    path: Path
    label: Label
    flags: List[Flag]



