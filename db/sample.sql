-- Sample users
INSERT INTO users(username, password, dp, email, fname, lname)
  VALUES('drjc', 'whereisthegreensheep', NULL, 'james.r.curran@sydney.edu.au', 'James', 'Curran');

INSERT INTO users(username, password, dp, email, fname, lname)
  VALUES('impendingnicky', 'kneecaps@reforde_stroy', NULL, 'summerschool@ncss.edu.au', 'Nicky', 'Kneecapper');

INSERT INTO users(username, password, dp, email, fname, lname)
  VALUES('tomtom', 'james', NULL, 'thomas.m.curran@sscn.edu.au', 'Thomas', 'Curran');

INSERT INTO users(username, password, dp, email, fname, lname)
  VALUES('test', 'tset', NULL, 'test@test.test', 'Mr', 'Test');

-- Sample locations
INSERT INTO locations(name, description, picture, uploader, address, latitude, longitude)
  VALUES('SIT', 'School of Information Technologies', 'sit.jpg', 1, 'USyd', -33.89, 151.2);

INSERT INTO locations(name, description, picture, uploader, address, latitude, longitude)
  VALUES('UNSW', 'Trash', 'unsw.jpg', 1, 'nowhere', -33.91, 151.2);

INSERT INTO locations(name, description, picture, uploader, address, latitude, longitude)
  VALUES('The Womens College', 'Cool place', 'womens_college.jpg', 2, 'USyd', -33.89, 151.2);

INSERT INTO locations(name, description, picture, uploader, address, latitude, longitude)
  VALUES('The mens College', 'Cool place', 'womens_college.jpg', 5, 'USyd', -33.89, 151.2);

-- Sample tags
INSERT INTO tags(name, place)
  VALUES('Univeristy', 1);

INSERT INTO tags(name, place)
  VALUES('Univeristy', 2);

INSERT INTO tags(name, place)
  VALUES('Trash', 2);

INSERT INTO tags(name, place)
  VALUES('SLEEP', 3);

-- Sample ratings
INSERT INTO ratings(place, score, user)
  VALUES(1, 5, 1);

INSERT INTO ratings(place, score, user)
  VALUES(2, 1, 1);
