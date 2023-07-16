import psycopg2

def get_postgresql_connection():
    try:
        dbname = 'watermarks'
        user = 'postgres'
        host = 'localhost'
        password = '123456'
        connectStr = "dbname='" + dbname + "' user='" + user + "' host='" + host + "' password='" + password + "'"
        connection = psycopg2.connect(connectStr)
        return connection
    except:
        print("Unable to connect to the database")
    return None

if __name__ == '__main__':
    connection = get_postgresql_connection()

    # cursor to iterate over data and not load all data into memory at once
    cursor = connection.cursor()

    sql = "SELECT * FROM TABLE"

    cursor.execute(sql)
    result = cursor.fetchone()

    # Example for using the cursor
    while result:
        a = result[0]
        b = result[1]
        result = cursor.fetchone()
