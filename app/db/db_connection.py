import psycopg2
import psycopg2.extras
from dotenv import dotenv_values
import os

# config = dotenv_values("../.env")

def get_connection():
    
    if 'DB_HOST' in os.environ :
        db_host = os.environ['DB_HOST']
    else:
        db_host = "localhost"
        
    db_config = {
        "host": db_host,
        "port": 5432,
        "dbname": "koujyou_db",
        "user": "postgres",
        "password": "Elkinpg1"
    }

    return psycopg2.connect(**db_config)