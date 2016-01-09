import sqlite3

class DatabaseConnection:
    def connect(self):
        self.conn = sqlite3.connect('something.db')

    def run_sql(self, sql):
        cur = self.conn.execute(sql)
        anything = cur.fetchone()
        print(anything)
