from connect import get_connection

conn = get_connection()
if conn:
    print("Успешное подключение к PostgreSQL!")
    conn.close()
else:
    print("Не удалось подключиться к базе данных.")