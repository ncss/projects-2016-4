import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

with open('sample.sql') as sql_file:
    sql = sql_file.read()
    cur.executescript(sql)

conn.close()
