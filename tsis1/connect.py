import psycopg2
from config import HOST, DATABASE, USER, PASSWORD, PORT


def get_connection():
    try:
        connection = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        return connection

    except psycopg2.Error as error:
        print("Database connection error:", error)
        return None


def connect():
    return get_connection()