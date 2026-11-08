import psycopg2
from config import HOST, DATABASE, USER, PASSWORD, PORT

def get_connection():
    return psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        port=PORT
    )