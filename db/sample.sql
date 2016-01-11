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
  VALUES('univeristy', 1);

INSERT INTO tags(name, place)
  VALUES('univeristy', 2);

INSERT INTO tags(name, place)
  VALUES('trash', 2);

INSERT INTO tags(name, place)
  VALUES('sleep', 3);

-- Sample ratings
INSERT INTO ratings(place, score, user)
  VALUES(1, 5, 1);

INSERT INTO ratings(place, score, user)
  VALUES(2, 1, 1);

-- Sample comments
INSERT INTO comments(author, comment, place)
  VALUES(1, 'Its like there are only two people here', 2);

INSERT INTO comments(author, comment, place)
  VALUES(4, 'Where is the green sheep?', 1);
INSERT INTO "comments" VALUES(1,1,'Its like there are only two people here',2);
INSERT INTO "comments" VALUES(2,4,'Where is the green sheep?',1);
INSERT INTO "locations" VALUES(1,'SIT','School of Information Technologies','sit.jpg',1,'USyd',-33.89,151.2);
INSERT INTO "locations" VALUES(2,'UNSW','Trash','unsw.jpg',1,'nowhere',-33.91,151.2);
INSERT INTO "locations" VALUES(3,'The Womens College','Cool place','womens_college.jpg',2,'USyd',-33.89,151.2);
INSERT INTO "locations" VALUES(4,'The mens College','Cool place','womens_college.jpg',5,'USyd',-33.89,151.2);
INSERT INTO "ratings" VALUES(1,5,1);
INSERT INTO "ratings" VALUES(2,1,1);
INSERT INTO "tags" VALUES(1,'univeristy',1);
INSERT INTO "tags" VALUES(2,'univeristy',2);
INSERT INTO "tags" VALUES(3,'trash',2);
INSERT INTO "tags" VALUES(4,'sleep',3);
INSERT INTO "users" VALUES(1,'drjc','whereisthegreensheep',NULL,'james.r.curran@sydney.edu.au','James','Curran');
INSERT INTO "users" VALUES(2,'impendingnicky','kneecaps@reforde_stroy',NULL,'summerschool@ncss.edu.au','Nicky','Kneecapper');
INSERT INTO "users" VALUES(3,'tomtom','james',NULL,'thomas.m.curran@sscn.edu.au','Thomas','Curran');
INSERT INTO "users" VALUES(4,'test','tset',NULL,'test@test.test','Mr','Test');
