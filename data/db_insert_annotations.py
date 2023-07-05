import psycopg2
import os
from typing import List
from data.connect_postgres import get_postgresql_connection
from annotation import Flag
from load_annotations import parse_raw_annotations, load_raw_annotations


def insert_annotations_to_db(cursor, annotations):
    for annotation in annotations:
        print("path: {}".format(os.path.join(annotation.path.folder_name, annotation.path.file_name)))
        # Insert into raw_image table
        cursor.execute(
            """
            INSERT INTO raw_image (id, path, annotation_id, geographical_region, text_in_image, text_on_watermark, incomplete, multiple_bounding_boxes, no_bounding_boxes, lines_in_bounding_boxes, ruler_in_bounding_boxes, other_markings_in_bounding_boxes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (annotation.id,
            os.path.join(annotation.path.folder_name, annotation.path.file_name),
            annotation.source_unique_id,
            annotation.path.geographical_source.value,
            any(flag == Flag.TII for flag in annotation.flags),
            any(flag == Flag.TOW for flag in annotation.flags),
            any(flag == Flag.IW for flag in annotation.flags),
            any(flag == Flag.MBB for flag in annotation.flags),
            any(flag == Flag.NBB for flag in annotation.flags),
            any(flag == Flag.SLBB for flag in annotation.flags),
            any(flag == Flag.RBB for flag in annotation.flags),
            any(flag == Flag.OMBB for flag in annotation.flags))
        )

if __name__ == 'main':
    raw_annotations = load_raw_annotations()
    annotations = parse_raw_annotations(raw_annotations)
    connection = get_postgresql_connection()
    cursor = connection.cursor()

    insert_annotations_to_db(cursor, annotations)