import psycopg2

load_config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432'
}

try:
    connection = psycopg2.connect(**load_config)
    print("succesfull connection")
    connection.close()
except Exception as error:
    print(f"Failed connection: {error}")