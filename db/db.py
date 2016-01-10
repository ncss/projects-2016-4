import sqlite3

conn = sqlite3.connect('db/database.db')


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
            WHERE username = ?''', (username,))
        res = cur.fetchone()
        if res:
            return User(*res)

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
            WHERE username = ?''', (password, self.username))
        self.password = password

    def change_email(self, email):
        conn.execute('''UPDATE users
            SET email = ?
            WHERE username = ?''', (email, self.username))
        self.email = email

    def change_username(self, username):
        conn.execute('''
            UPDATE users
            SET username = ?
            WHERE username = ?''', (username, self.username))
        self.username = username

    @staticmethod
    def create(username, password, dp, email, fname, lname):
        conn.execute('''INSERT INTO users (username, password, dp, email, fname, lname)
            VALUES(?, ?, ?, ?, ?, ?)''',
            (username, password, dp, email, fname, lname)
        )
        cur = conn.execute('''SELECT id FROM users WHERE username = ?''', (username,))
        res = cur.fetchone()
        return User(username, password, email, res[0])

    def save(self):
        conn.execute('''UPDATE users
            SET password = ?, email = ?
            WHERE username = ?
        ''', (self.password, self.email, self.username))

    @staticmethod
    def delete(username):
        conn.execute('DELETE FROM users WHERE username = ?', (username,))


class Location:
    def __init__(self, name, description, picture, uploader, address, longitude, latitude, id=None):
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
        conn.execute('''
            INSERT INTO locations(name, description, picture, uploader, address, longitude, latitude)
            VALUES(?, ?, ?, ?, ?, ?, ?);
        ''', (name, description, picture, uploader, address, longitude, latitude))
        return Location(name, description, picture, uploader, address, longitude, latitude)

    def change_location(self, address, longitude, latitude):
        conn.execute('''
            UPDATE location
            SET address = ?, longitude = ?, latitude = ?
            WHERE id = ?;''', (address, longitude, latitude, self.id))

    @staticmethod
    def find_id(id):
        cur = conn.execute('''
            SELECT name, description, picture, uploader, address, longitude, latitude FROM locations
             WHERE id = ?
             ''', (id,))
        res = cur.fetchone()
        if res:
            return Location(*res)

    @staticmethod
    def find_name(name):
        cur = conn.execute('''
            SELECT name, description, picture, uploader, address, longitude, latitude, id FROM locations
             WHERE name = ?
             ''', (name,))
        res = cur.fetchone()
        if res:
            location = Location(*res)
            return location

    @staticmethod
    def findall():
        cur = conn.execute('SELECT name, description, picture, uploader, address, longitude, latitude FROM locations')
        res = []
        for row in cur:
            res.append(Location(*row))
        return res

    @staticmethod
    def delete(id):
        conn.execute('DELETE FROM locations WHERE id = ?', (id,))

    def save(self):
        conn.execute('''UPDATE locations
            SET name = ?, description = ?, picture = ?, uploader = ?, address = ?, longitude = ?, latitude = ?
            WHERE id = ?
        ''', (self.name, self.description, self.picture, self.uploader, self.address, self.longitude, self.latitude, self.id))


class Tag:
    def __init__(self, name, place):
        self.name = name
        self.place = place

    @staticmethod
    def create(name, place):
        conn.execute('''INSERT INTO tags(name, place)
            VALUES(?, ?)''', (name, place))

