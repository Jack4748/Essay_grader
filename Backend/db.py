import psycopg2


def get_db_connection(url):
    try:
        connection = psycopg2.connect(url)
        return connection
    except Exception as error:
        print("Error connecting to the database:",error)
        raise error 


def create_metrics_table(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics_db (
                essay_id INTEGER PRIMARY KEY REFERENCES essay_db(essay_id),
                focus_and_development FLOAT,
                content_development FLOAT,
                organisation FLOAT,
                language_use FLOAT,
                Holistic_Score FLOAT
            )
        """)
    connection.commit()


def create_essay_table(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS essay_db (
                directory TEXT NOT NULL,
                essay_id INTEGER NOT NULL PRIMARY KEY
            )
        """)
    connection.commit()
