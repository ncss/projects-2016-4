import sqlite3
import os

if os.path.exists('database.db'):
    os.remove('database.db')
    print('File removed')

conn = sqlite3.connect('database.db')
cur = conn.cursor()

with open('db.sql') as sql_file:
    sql = sql_file.read()
    cur.executescript(sql)

conn.close()
