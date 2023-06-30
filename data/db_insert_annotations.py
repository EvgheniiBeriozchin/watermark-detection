import psycopg2
from typing import List
from connect_postgres import get_postgresql_connection
from annotation import Flag
from load_annotations import parse_raw_annotations, load_raw_annotations


def insert_annotations_to_db(annotations):
    try:
        # connect to the PostgreSQL server
        connection = get_postgresql_connection()
        cursor = connection.cursor()

        print(len(annotations))

        for annotation in annotations:
            print(annotation)
            # Insert into raw_image table
            cursor.execute(
                """
                INSERT INTO raw_image (id, path, annotation_id, geographical_region, test_in_image, text_on_watermark, incomplete, multiple_bounding_boxes, no_bounding_boxes, lines_in_bounding_boxes, ruler_in_bounding_boxes, other_markings_in_bounding_boxes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (annotation.id,
                 annotation.path.folder_name + "/" + annotation.path.file_name,
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
            print("Executed")


            # Insert into bounding_box table
            for bounding_box in annotation.bounding_boxes:
                cursor.execute(
                    """
                    INSERT INTO bounding_box (id, raw_image_id, x, y, width, height, rotation, label)
                    VALUES (DEFAULT, (SELECT id FROM raw_image WHERE path = %s), %s, %s, %s, %s, %s, %s)
                    """,
                    (annotation.path.folder_name + "/" + annotation.path.file_name, bounding_box.x, bounding_box.y, bounding_box.width, bounding_box.height, bounding_box.rotation, bounding_box.label.value)
                )

        # close communication with the PostgreSQL database server
        cursor.close()
        # commit the changes
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()

if __name__ == 'main':
    raw_annotations = load_raw_annotations()
    annotations = parse_raw_annotations(raw_annotations)
    insert_annotations_to_db(annotations)