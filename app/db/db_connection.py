import psycopg2
import psycopg2.extras

def get_connection():

    db_config = {
        "host": "localhost",
        "port": 5432,
        "dbname": "koujyou_db",
        "user": "postgres",
        "password": "Elkinpg1"
    }

    return psycopg2.connect(**db_config)