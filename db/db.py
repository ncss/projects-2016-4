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
        conn.commit()
        self.password = password

    def change_email(self, email):
        conn.execute('''UPDATE users
            SET email = ?
            WHERE username = ?''', (email, self.username))
        conn.commit()
        self.email = email

    def change_username(self, username):
        conn.execute('''
            UPDATE users
            SET username = ?
            WHERE username = ?''', (username, self.username))
        conn.commit()
        self.username = username

    @staticmethod
    def create(username, password, dp, email, fname, lname):
        conn.execute('''INSERT INTO users (username, password, dp, email, fname, lname)
            VALUES(?, ?, ?, ?, ?, ?)''',
            (username, password, dp, email, fname, lname)
        )
        cur = conn.execute('''SELECT id FROM users WHERE username = ?''', (username,))
        res = cur.fetchone()
        conn.commit()
        return User(username, password, email, res[0])

    def save(self):
        conn.execute('''UPDATE users
            SET password = ?, email = ?
            WHERE username = ?
        ''', (self.password, self.email, self.username))
        conn.commit()

    @staticmethod
    def delete(username):
        conn.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()


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

    def __repr__(self):
        return "Location(%s)" % self.name

    @staticmethod
    def create(name, description, picture, uploader, address, latitude, longitude):
        conn.execute('''
            INSERT INTO locations(name, description, picture, uploader, address, latitude, longitude)
            VALUES(?, ?, ?, ?, ?, ?, ?);
        ''', (name, description, picture, uploader, address, latitude, longitude))
        conn.commit()
        return Location(name, description, picture, uploader, address, latitude, longitude)

    def change_location(self, address, longitude, latitude):
        conn.execute('''
            UPDATE location
            SET address = ?, longitude = ?, latitude = ?
            WHERE id = ?;''', (address, longitude, latitude, self.id))
        conn.commit()

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
             WHERE name =  ?
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
        conn.commit()

    def save(self):
        conn.execute('''UPDATE locations
            SET name = ?, description = ?, picture = ?, uploader = ?, address = ?, longitude = ?, latitude = ?
            WHERE id = ?
        ''', (self.name, self.description, self.picture, self.uploader, self.address, self.longitude, self.latitude, self.id))
        conn.commit()

    @staticmethod
    def search_name(name):
        cur = conn.execute('''
            SELECT name, description, picture, uploader, address, longitude, latitude, id FROM locations
            WHERE name LIKE  '%' || ? || '%'
            ''', (name,))
        res = []
        for i in cur.fetchall():
            res.append(Location(*i))
        return res

    @staticmethod
    def search_tag(tag_name):
        cur = conn.execute('''
          SELECT l.name, description, picture, uploader, address, longitude, latitude, l.id FROM locations l
          JOIN  tags t ON l.id = t.place
          WHERE t.name = ?
          ''', (tag_name,))
        return [Location(*row) for row in cur.fetchall()]

    def get_tags(self):
        return Tag.find_from_place(self.id)

    def add_tag(self, name):
        return Tag.create_tag(name, self.id)

class Tag:
    def __init__(self, name, place):
        self.name = name
        self.place = place

    def __repr__(self):
        return 'Tag("%s")' % self.name

    @staticmethod
    def create_tag(name, place):
        conn.execute('''INSERT INTO tags(name, place)
            VALUES(?, ?);''', (name, place))
        conn.commit()
        return Tag(name, place)

    @staticmethod
    def find_tag(name):
        cur = conn.execute('''
          SELECT name, place FROM tags
          WHERE name = ?
        ''', (name,))
        res = cur.fetchone()

        if res:
            return Tag(*res)

    @staticmethod
    def find_from_place(place):
        cur = conn.execute('''
          SELECT name
          FROM tags
          WHERE place = ?
        ''', (place,))

        res = []
        for name in cur.fetchall():
            res.append(Tag(name, place))
        return res

    @staticmethod
    def delete_tag(name, place):
        conn.execute('''
          DELETE FROM tags
          WHERE place = ? AND name = ?
          ''', (place, name))
        conn.commit()


    def delete(self):
        return Tag.delete_tag(self.name, self.place)

