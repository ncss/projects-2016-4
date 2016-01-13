import sqlite3
from math import sqrt

conn = sqlite3.connect('db/database.db')


def run_sql(sql):
    cur = conn.execute(sql)
    anything = cur.fetchone()
    return anything


class User:
    def __init__(self, username, password, dp, email, fname, lname, id=None):
        self.username = username
        self.password = password
        self.dp = dp
        self.email = email
        self.fname = fname
        self.lname = lname
        self.id = id

    @staticmethod
    def find(username):
        cur = conn.execute('SELECT username, password, dp, email, fname, lname, id FROM users WHERE username = ?',
                           (username,))
        res = cur.fetchone()
        if res:
            return User(*res)

    @property
    def full_name(self):
        if self.fname and self.lname:
            return self.fname + ' ' + self.lname
        elif self.fname:
            return self.fname
        elif self.lname:
            return self.lname
        else:
            return self.username

    @staticmethod
    def get_email(email):
        cur = conn.execute('SELECT email FROM users WHERE email = ?', (email,))
        res = cur.fetchone()
        if res:
            return email
        return False

    @staticmethod
    def findall():
        cur = conn.execute('SELECT username, password, email, id FROM users')
        res = []
        for row in cur:
            res.append(User(*row))
        return res

    def change_password(self, password):
        conn.execute('UPDATE users SET password = ? WHERE username = ?', (password, self.username))
        conn.commit()
        self.password = password

    def change_email(self, email):
        conn.execute('UPDATE users SET email = ? WHERE username = ?', (email, self.username))
        conn.commit()
        self.email = email

    def change_username(self, username):
        conn.execute('UPDATE users SET username = ? WHERE username = ?', (username, self.username))
        conn.commit()
        self.username = username

    def create(self):
        cur = conn.execute('''SELECT username, password, dp, email, fname, lname FROM users
                           WHERE username = ? OR email = ?''', (self.username, self.email))
        res = cur.fetchone()

        if res is None:
            conn.execute('INSERT INTO users(username, password, dp, email, fname, lname) VALUES(?, ?, ?, ?, ?, ?)',
                         (self.username, self.password, self.dp, self.email, self.fname, self.lname))
            conn.commit()
            return User.find(self.username)
        else:
            return False

    def save(self):
        conn.execute('UPDATE users SET password = ?, email = ? WHERE username = ?',
                     (self.password, self.email, self.username))
        conn.commit()

    @staticmethod
    def delete(username):
        conn.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()

    @staticmethod
    def all_locations():
        pass

    @staticmethod
    def search_tag(tag_name):
        cur = conn.execute('''SELECT l.name, description, picture, uploader, address, longitude, latitude, l.id
                           FROM locations l JOIN  tags t ON l.id = t.place WHERE t.name = ?''', (tag_name,))
        return [Location(*row) for row in cur.fetchall()]

    def get_tags(self):
        return Tag.find_from_place(self.id)

    def add_tag(self, name):
        return Tag(name, self.id).create()


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
        return "Location({})".format(self.name)

    def create(self):
        conn.execute('''INSERT INTO locations(name, description, picture, uploader, address, latitude, longitude)
                     VALUES(?, ?, ?, ?, ?, ?, ?);''',
                     (self.name, self.description, self.picture, self.uploader, self.address, self.latitude,
                      self.longitude))
        conn.commit()
        id = conn.execute('SELECT MAX(id) FROM locations').fetchone()[0]
        return Location(self.name, self.description, self.picture, self.uploader, self.address,
                        self.longitude, self.latitude, self.id)

    @staticmethod
    def find_user_locations(user_id):
        cur = conn.execute('''SELECT name, description, picture, uploader, address, latitude, longitude, id
                           FROM locations WHERE uploader = ?''', (user_id,))
        res = []
        for row in cur:
            res.append(Location(*row))
        return res

    @staticmethod
    def change_location(id, name, description, picture, address, latitude, longitude):
        conn.execute('''UPDATE locations
                     SET name = ?, description = ?, picture = ?, address = ?, latitude = ?, longitude = ?
                     WHERE id = ?;''', (name, description, picture, address, latitude, longitude, id))
        conn.commit()

    @staticmethod
    def find_id(id):
        cur = conn.execute('''SELECT name, description, picture, uploader, address, longitude, latitude, id
                           FROM locations WHERE id = ?''', (id,))
        res = cur.fetchone()
        if res:
            return Location(*res)

    @staticmethod
    def find_name(name):
        cur = conn.execute('''SELECT name, description, picture, uploader, address, longitude, latitude, id
                           FROM locations WHERE name =  ?''', (name,))
        res = cur.fetchone()
        if res:
            location = Location(*res)
            return location

    @staticmethod
    def findall():
        cur = conn.execute('''SELECT name, description, picture, uploader, address, longitude, latitude, id
                           FROM locations''')
        res = []
        for row in cur:
            res.append(Location(*row))
        return res

    @staticmethod
    def delete(id):
        conn.execute('DELETE FROM locations WHERE id = ?', (id,))
        conn.commit()

    def save(self):
        conn.execute('''UPDATE locations SET name = ?, description = ?, picture = ?, uploader = ?, address = ?,
                     longitude = ?, latitude = ? WHERE id = ?''',
                     (self.name, self.description, self.picture,self.uploader, self.address, self.longitude,
                      self.latitude, self.id))
        conn.commit()

    @staticmethod
    def search_name(name):
        cur = conn.execute('''SELECT name, description, picture, uploader, address, longitude, latitude, id
                           FROM locations WHERE (address LIKE '%' || ? || '%' OR name LIKE '%' || ? || '%')''',
                           (name, name))
        res = []
        for i in cur.fetchall():
            res.append(Location(*i))
        return res

    @staticmethod
    def search_tag(tag_name):
        cur = conn.execute('''SELECT l.name, description, picture, uploader, address, longitude, latitude, l.id
                           FROM locations l JOIN tags t ON l.id = t.place WHERE t.name = ?''', (tag_name,))
        return [Location(*row) for row in cur.fetchall()]

    @staticmethod
    def search(tag_name, location_name):
        cur = conn.execute('''SELECT l.name, description, picture, uploader, address, longitude, latitude, l.id
                           FROM locations l JOIN tags t ON l.id = t.place
                           WHERE t.name = ? AND (address LIKE '%' || ? || '%' OR l.name LIKE '%' || ? || '%')''',
                           (tag_name, location_name, location_name))
        return [Location(*row) for row in cur.fetchall()]

    @staticmethod
    def search_address(address):
        cur = conn.execute('''SELECT l.name, description, picture, uploader, address, longitude, latitude, l.id
                           FROM locations l WHERE address LIKE '%' || ? || '%' ''', (address,))
        return [Location(*row) for row in cur.fetchall()]

    def get_tags(self):
        return Tag.find_from_place(self.id)

    @property
    def avg_rating(self):
        cur = conn.execute('SELECT score FROM ratings WHERE place = ?', (self.id,))
        res = cur.fetchall()

        total = 0
        num_of_ratings = 0
        for i in res:
            if type(i[0]) is int:
                total += i[0]
                num_of_ratings += 1

        if total != 0:
            average = total/num_of_ratings
            return average

    def get_user_rating(self, user):
        cur = conn.execute('SELECT score FROM ratings r WHERE user = ? AND place = ?', (user, self.id))

        res = cur.fetchone()
        if res:
            try:
                return int(res[0])
            except ValueError:
                return

    def distance_from(self, latitude, longitude):
        return sqrt((latitude-self.latitude)**2+(longitude-self.longitude)**2) * 95.59


class Tag:
    def __init__(self, name, place):
        self.name = name
        self.place = place

    def __repr__(self):
        return 'Tag("{}")'.format(self.name)

    def create(self):
        conn.execute('INSERT INTO tags(name, place) VALUES(?, ?);', (self.name, self.place))
        conn.commit()
        return Tag(self.name, self.place)

    @staticmethod
    def find_tag(name):
        cur = conn.execute('SELECT name, place FROM tags WHERE name = ?', (name,))
        res = cur.fetchone()

        if res:
            return Tag(*res)

    @staticmethod
    def find_from_place(place):
        cur = conn.execute('SELECT name FROM tags WHERE place = ?', (place,))

        res = []
        for name in cur.fetchall():
            res.append(Tag(name, place))
        return res

    @staticmethod
    def delete_tag(name, place):
        conn.execute('DELETE FROM tags WHERE place = ? AND name = ?', (place, name))
        conn.commit()

    def delete(self):
        return Tag.delete_tag(self.name, self.place)


class Rating:
    def __init__(self, place, score, user):
        self.place = place
        self.score = score
        self.user = user

    def create(self):
        cur = conn.execute('SELECT place, score, user FROM ratings WHERE user = ? AND place = ?',
            (self.user, self.place))
        res = cur.fetchone()
        if res is None:
            conn.execute('INSERT INTO ratings(place, score, user) VALUES(?, ?, ?);',
                (self.place, self.score, self.user))
            conn.commit()
        else:
            conn.execute('UPDATE ratings SET score = ? WHERE user = ?', (self.score, self.user))
            conn.commit()
        return Rating(self.place, self.score, self.user)

    @staticmethod
    def find_user(user):
        cur = conn.execute('SELECT place, score, user FROM ratings WHERE user = ?', (user,))

        res = cur.fetchone()
        if res:
            return Rating(*res)


class Comment:
    def __init__(self, author, comment, place, id=None):
        self.author = author
        self.comment = comment
        self.place = place
        self.id = id

    def create(self):
        conn.execute('INSERT INTO comments(author, comment, place) VALUES(?, ?, ?);',
                     (self.author, self.comment, self.place))
        conn.commit()
        id = conn.execute('SELECT MAX(id) FROM locations').fetchone()[0]
        return Comment(self.author, self.comment, self.place, id=id)

    @staticmethod
    def find_author(author):
        res = []
        cur = conn.execute('SELECT author, comment, place, id FROM comments WHERE author=?', (author,))
        for row in cur.fetchall():
            res.append(Comment(*row))
        return res

    @staticmethod
    def find_place(place):
        res = []
        cur = conn.execute('SELECT author, comment, place, id FROM comments WHERE place=?', (place,))
        for row in cur.fetchall():
            res.append(Comment(*row))
        return res

    @staticmethod
    def get_author_comment(user_id):
        cur = conn.execute('SELECT username FROM users u JOIN comments c ON c.author = u.id WHERE u.id =?', (user_id,))
        res = cur.fetchone()
        if res:
            return res[0]
