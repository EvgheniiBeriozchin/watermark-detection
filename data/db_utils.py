import psycopg2
from typing import Optional, List
from data.connect_postgres import get_postgresql_connection
from annotation import Flag, Label

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
            conditions.append("bounding_box_id IN (SELECT id FROM bounding_box WHERE label = %s)")
        if flags:
            flag_conditions = ["bounding_box_id IN (SELECT id FROM bounding_box WHERE label = %s)" for flag in flags]
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

def clean_db(cursor):
    cursor.execute("DROP TABLE raw_image;")
    cursor.execute("DROP TABLE bounding_box;")
    cursor.execute("DROP TABLE image;")
    cursor.execute("DROP TABLE preprocessed_image;")
    cursor.execute("DROP TABLE encoding;")