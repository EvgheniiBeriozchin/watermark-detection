import psycopg2

def get_postgresql_connection():
    try:
        dbname = ''
        user = ''
        host = ''
        password = ''
        connectStr = "dbname='" + dbname + "' user='" + user + "' host='" + host + "' password='" + password + "'"
        connection = psycopg2.connect(connectStr)
        return connection
    except:
        print("Unable to connect to the database")
    return None
