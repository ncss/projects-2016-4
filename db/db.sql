CREATE TABLE users (
    id INTEGER NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    dp TEXT,
    email TEXT NOT NULL,
    fname TEXT,
    lname TEXT,
    UNIQUE (username, email),
    PRIMARY KEY (id)
);

CREATE TABLE locations (
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    picture TEXT NOT NULL,
    uploader INTEGER NOT NULL,
    address TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (uploader) REFERENCES users (id)
);

CREATE TABLE tags (
  id INTEGER NOT NULL,
  name TEXT NOT NULL,
  place TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (place) REFERENCES locations(id)
);

CREATE TABLE ratings (
  id INTEGER NOT NULL,
  place INTEGER NOT NULL,
  score INTEGER NOT NULL,
  user INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (place) REFERENCES locations (id),
  FOREIGN KEY (user) REFERENCES users(id)
);