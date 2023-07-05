import psycopg2
from connect_postgres import get_postgresql_connection
from ..constants import PROCESSED_IMAGE_TRAIN_PATH, PROCESSED_IMAGE_VAL_PATH
from ..annotation import Label

def insert_bounding_box_to_db(cursor, annotation, bounding_box):
    cursor.execute(
        """
        INSERT INTO bounding_box (raw_image_id, x, y, width, height, rotation, label)
        VALUES ((SELECT id FROM raw_image WHERE path = %s), %s, %s, %s, %s, %s, %s)
        """,
        (annotation.path.folder_name + "/" + annotation.path.file_name, bounding_box.x, bounding_box.y, bounding_box.width, bounding_box.height, bounding_box.rotation, bounding_box.label.value)
    )

    return cursor.fetchone()[0]

def insert_cut_image_to_db(cursor, cropped_image_path, bounding_box_id):
    cursor.execute(
        """
        INSERT INTO image (bounding_box_id, path)
        VALUES (%s, %s)
        RETURNING id;
        """,
        (bounding_box_id, cropped_image_path)
    )

    return cursor.fetchone()[0]

def insert_processed_image_to_db(cursor, processed_image_path, cut_image_id):
    cursor.execute(
        """
        INSERT INTO preprocessed_image (image_id, path)
        VALUES (%s, %s)
        RETURNING id;
        """,
        (cut_image_id, processed_image_path)
    )

    return cursor.fetchone()[0]
