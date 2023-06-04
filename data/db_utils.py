import psycopg2
from typing import Optional, List
from psycopg2.extras import execute_values
from connect_postgres import get_postgresql_connection
from annotation import Annotation, BoundingBox, Flag, GeographicalSource, Label, Path
from load_annotations import parse_raw_annotations


def insert_annotations_to_db(annotations):
    try:
        # connect to the PostgreSQL server
        connection = get_postgresql_connection()
        cursor = connection.cursor()

        for annotation in annotations:
            # Insert into RawImage table
            cursor.execute(
                """
                INSERT INTO RawImage (id, path, annotation_id, geographical_region, text_in_image, text_on_watermark, incomplete, multiple_bounding_boxes, no_bounding_boxes, lines_in_bounding_boxes, ruler_in_bounding_boxes, other_markings_in_bounding_boxes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (annotation.id, annotation.path.folder_name + "/" + annotation.path.file_name, annotation.source_unique_id, annotation.path.geographical_source.value,
                any(flag == Flag.TEXT_IN_IMAGE for flag in annotation.flags), any(flag == Flag.TEXT_ON_WATERMARK for flag in annotation.flags), any(flag == Flag.INCOMPLETE for flag in annotation.flags),
                any(flag == Flag.MULTIPLE_BOUNDING_BOXES for flag in annotation.flags), any(flag == Flag.NO_BOUNDING_BOXES for flag in annotation.flags),
                any(flag == Flag.LINES_IN_BOUNDING_BOXES for flag in annotation.flags), any(flag == Flag.RULER_IN_BOUNDING_BOXES for flag in annotation.flags),
                any(flag == Flag.OTHER_MARKINGS_IN_BOUNDING_BOXES for flag in annotation.flags))
            )


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
#def insert_encoding_to_db():
