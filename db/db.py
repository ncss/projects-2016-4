import sqlite3

class DatabaseConnection:
    def connect(self):
        self.conn = sqlite3.connect('database.db')

    def run_sql(self, sql):
        cur = self.conn.execute(sql)
        anything = cur.fetchone()
        print(anything)

class User:
    def __init__(self, conn, id, username, password, email):
        self.id = id
        self.conn = conn
        self.username = username
        self.password = password
        self.email = email

    def find(self, username):
        cur = self.conn.execute('''
            SELECT id, username, password, email
            FROM users
            WHERE username = ?''', (username,)
        )

    def change_password(self, password):
        cur = self.conn.execute('''
            UPDATE users
            SET password = ?
            WHERE id = ?''', (password, self.id)
        )
        self.password = password

    def change_email(self, email):
        cur = self.conn.execute('''
            UPDATE users
            SET email = ?
            WHERE id = ?''', (email, self.id)
        )
        self.email = email



