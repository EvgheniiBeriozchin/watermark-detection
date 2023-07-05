from data.db_insert_annotations import insert_annotations_to_db
from data.create_table import create_tables
from data.db_utils import clean_db
from utils import remove_processed_data
from load_annotations import load_raw_annotations, parse_raw_annotations
from preprocess_images import preprocess_images
from utils import check_folders_exist
from data.connect_postgres import get_postgresql_connection


if __name__ == '__main__':
    connection = get_postgresql_connection()
    cursor = connection.cursor()

    raw_annotations = load_raw_annotations()
    annotations = parse_raw_annotations(raw_annotations)
    insert_annotations_to_db(cursor, annotations)
    
    check_folders_exist(annotations)
    
    remove_processed_data()
    clean_db(cursor)
    create_tables(cursor)

    preprocess_images(cursor, annotations)