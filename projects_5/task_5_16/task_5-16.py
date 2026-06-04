import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="example",
        database="testdb"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM students;")
    result = cursor.fetchone()
    print(f"Количество студентов: {result[0]}")
    cursor.close()
    connection.close()
except Exception as error:
    print(f"Ошибка: {error}")
