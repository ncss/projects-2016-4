import sqlite3

conn = sqlite3.connect('database.db')

def run_sql(sql):
    cur = conn.execute(sql)
    anything = cur.fetchone()
    return anything

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

class Location:
    def __init__(self, id, name, description, picture, uploader, address, latitude, longitude):
        self.id = id
        self.name = name
        self.description = description
        self.picture = picture
        self.uploader = uploader
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def create(name, description, picture, uploader, address, longitude, latitude):
        cur = conn.execute('''
            INSERT INTO locations(name, description, picture, uploader, address, longitude, latitude)
            VALUES(?, ?, ?, ?, ?, ?, ?);
        ''', (name, description, picture, uploader, address, longitude, latitude))

    def change_location(self, address, longitude, latitude):
        cur = conn.execute('''
            UPDATE location
            SET address = ?, longitude = ?, latitude = ?
            WHERE id = ?;''', (address, longitude, latitude, self.id))

    @staticmethod
    def find(id):
        cur =  conn.execute('''
            SELECT * FROM locations
             WHERE id = ?
             ''', (id,))
        fetch = cur.fetchone()
        return fetch
