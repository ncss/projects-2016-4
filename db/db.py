import sqlite3

conn = sqlite3.connect('database.db')

def run_sql(sql):
    cur = conn.execute(sql)
    anything = cur.fetchone()
    return anything

class User:
    def __init__(self, username, password, email, id=None):
        self.username = username
        self.password = password
        self.email = email
        self.id = id

    @staticmethod
    def find(username):
        cur = conn.execute('''
            SELECT username, password, email, id
            FROM users
            WHERE username = ?''', (username,)
        )
        return User(*cur.fetchone())

    @staticmethod
    def findall():
        cur = conn.execute('SELECT username, password, email, id FROM users')
        res = []
        for row in cur:
            res.append(User(*row))
        return res

    def change_password(self, password):
        conn.execute('''UPDATE users
            SET password = ?
            WHERE username = ?''', (password, self.username)
        )
        self.password = password

    def change_email(self, email):
        conn.execute('''UPDATE users
            SET email = ?
            WHERE username = ?''', (email, self.username)
        )
        self.email = email

    def change_username(self, username):
        conn.execute('''
            UPDATE users
            SET username = ?
            WHERE username = ?''', (username, self.username)
        )
        self.username = username

    def create(self):
        conn.execute('''INSERT INTO users (username, password, dp, email, fname, lname)
            VALUES(?, ?, NULL, ?, NULL, NULL)''',
            (self.username, self.password, self.email)
        )
        cur = conn.execute('''SELECT id FROM users WHERE username = ?''', (self.username,))
        res = cur.fetchone()
        self.id = res[0]


    def save(self):
        """cur = self.conn.execute('''UPDATE users
            SET password = ?, email = ?
            WHERE username ="""

    @staticmethod
    def delete(username):
        cur = conn.execute('DELETE FROM users WHERE username = ?', (username,))


class Location:
    def __init__(self, name, description, picture, uploader, address, longitude, latitude, id = None):
        self.name = name
        self.description = description
        self.picture = picture
        self.uploader = uploader
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.id = id

    @staticmethod
    def create(name, description, picture, uploader, address, longitude, latitude):
        cur = conn.execute('''
            INSERT INTO locations(name, description, picture, uploader, address, longitude, latitude)
            VALUES(?, ?, ?, ?, ?, ?, ?);
        ''', (name, description, picture, uploader, address, longitude, latitude))
        return Location(name, description, picture, uploader, address, longitude, latitude)

    def change_location(self, address, longitude, latitude):
        cur = conn.execute('''
            UPDATE location
            SET address = ?, longitude = ?, latitude = ?
            WHERE id = ?;''', (address, longitude, latitude, self.id))

    @staticmethod
    def find_id(id):
        cur =  conn.execute('''
            SELECT name, description, picture, uploader, address, longitude, latitude FROM locations
             WHERE id = ?
             ''', (id,))
        fetch = cur.fetchone()
        if fetch is not None:
            return Location(fetch[0], fetch[1], fetch[2], fetch[3], fetch[4], fetch[5], fetch[6])

    @staticmethod
    def find_name(name):
        cur =  conn.execute('''
            SELECT name, description, picture, uploader, address, longitude, latitude, id FROM locations
             WHERE name = ?
             ''', (name,))
        fetch = cur.fetchone()
        if fetch is not None:
            location =  Location(fetch[0], fetch[1], fetch[2], fetch[3], fetch[4], fetch[5], fetch[6])
            location.id = fetch[7]
            return location

    @staticmethod
    def findall():
        cur = conn.execute('SELECT  name, description, picture, uploader, address, longitude, latitude FROM locations')
        res = []
        for row in cur:
            res.append(Location(*row))
        return res

    @staticmethod
    def delete(id):
        cur = conn.execute('DELETE FROM locations WHERE id = ?', (id,))