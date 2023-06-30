import psycopg2
from connect_postgres import get_postgresql_connection


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
		CREATE TABLE raw_image (
                id SERIAL PRIMARY KEY,
                path TEXT UNIQUE,
                annotation_id TEXT UNIQUE,
                geographical_region VARCHAR(50),
                text_in_image BOOLEAN,
                text_on_watermark BOOLEAN,
                incomplete BOOLEAN,
                multiple_bounding_boxes BOOLEAN,
                no_bounding_boxes BOOLEAN,
                lines_in_bounding_boxes BOOLEAN,
                ruler_in_bounding_boxes BOOLEAN,
                other_markings_in_bounding_boxes BOOLEAN
                )
		""",
        """ CREATE TABLE bounding_box (
                id SERIAL PRIMARY KEY,
                raw_image_id INTEGER REFERENCES raw_image (id),
                x FLOAT,
                y FLOAT,
                width FLOAT,
                height FLOAT,
                rotation FLOAT,
                label VARCHAR(50)
                )
        """,
        """
		CREATE TABLE image (
                id SERIAL PRIMARY KEY,
                bounding_box_id INTEGER UNIQUE REFERENCES bounding_box (id),
                path TEXT UNIQUE
                )  
		""",
        """
		CREATE TABLE encoding (
                id SERIAL PRIMARY KEY,
                image_id INTEGER REFERENCES image (id),
                path TEXT UNIQUE,
                model_version TEXT
                )
		""")
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = get_postgresql_connection()
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
