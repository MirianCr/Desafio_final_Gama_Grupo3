import mysql.connector

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='dbpousada'
)

cursor = conn.cursor(buffered=True)
