import sqlite3
from venv import create

conn = sqlite3.connect('db.sqlite')

cursor = conn.cursor()

sql_query = """CREATE TABLE database(
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    website TEXT
    )"""
cursor.execute(sql_query)