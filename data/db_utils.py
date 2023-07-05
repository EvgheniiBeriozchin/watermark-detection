import psycopg2
from typing import Optional, List
from psycopg2.extras import execute_values
from connect_postgres import get_postgresql_connection
from annotation import Annotation, BoundingBox, Flag, GeographicalSource, Label, Path
from load_annotations import parse_raw_annotations, load_raw_annotations

from benchmarking.utils_benchmarking import get_test_paths


def insert_annotations_to_db(annotations):
    try:
        # connect to the PostgreSQL server
        connection = get_postgresql_connection()
        cursor = connection.cursor()

        print(len(annotations))

        for annotation in annotations:
            print(annotation)
            # Insert into RawImage table
            cursor.execute(
                """
                INSERT INTO RawImage (id, path, annotation_id, geographical_region, test_in_image, text_on_watermark, incomplete, multiple_bounding_boxes, no_bounding_boxes, lines_in_bounding_boxes, ruler_in_bounding_boxes, other_markings_in_bounding_boxes)
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


            # Insert into BoundingBox table
            for bounding_box in annotation.bounding_boxes:
                cursor.execute(
                    """
                    INSERT INTO BoundingBox (id, raw_image_id, x, y, width, height, rotation, label)
                    VALUES (DEFAULT, (SELECT id FROM RawImage WHERE path = %s), %s, %s, %s, %s, %s, %s)
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


def insert_testset_to_db(rootdir):
    try:
        # connect to the PostgreSQL server
        connection = get_postgresql_connection()
        cursor = connection.cursor()

        classlabels = get_test_paths(rootdir)

        for path, class_label in classlabels
            print(path, class_label)

            cursor.execute(
                """
                INSERT INTO TestSet (id, raw_image_id, path, category)
                VALUES (DEFAULT, (SELECT id FROM RawImage WHERE path = %s), %s, %s)                
                """,
                (path, path, class_label)
            )

        cursor.close()
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()


def query_images(label: Optional[Label], flags: List[Flag]):
    try:
        # connect to the PostgreSQL server
        connection = get_postgresql_connection()
        cursor = connection.cursor()

        # Build the SQL query dynamically based on the provided parameters
        query = "SELECT * FROM Image"
        conditions = []

        # Add conditions for label and flags if they are provided
        if label:
            conditions.append("bounding_box_id IN (SELECT id FROM BoundingBox WHERE label = %s)")
        if flags:
            flag_conditions = ["bounding_box_id IN (SELECT id FROM BoundingBox WHERE label = %s)" for flag in flags]
            conditions.append(" OR ".join(flag_conditions))

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Execute the query
        if label and flags:
            cursor.execute(query, (label.value,) + tuple(flag.value for flag in flags))
        elif label:
            cursor.execute(query, (label.value,))
        elif flags:
            cursor.execute(query, tuple(flag.value for flag in flags))

        results = cursor.fetchall()
        return results

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        connection.close()


# to be added

raw_annotations = load_raw_annotations()
annotations = parse_raw_annotations(raw_annotations)
insert_annotations_to_db(annotations)