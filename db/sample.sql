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
INSERT INTO "comments" VALUES(1,1,'Love it!! Definitely visiting again!! Thanks :)',1);
INSERT INTO "locations" VALUES(1,'Bea''s Of Bloomsbury','Bea''s of Bloomsbury is well-known for its afternoon teas, but it also does a mean selection of individual treats. It''s a great fan of the cake hybrid - there''s the townie (tart-brownie) and the duffin (the donut-muffin that they won a legal battle against Starbucks over) - and the raspberry chocolate layer cake and the peanut butter jelly slice are both divine. Plus, you can see the kitchen from the cafe seating area, which is always fun.','b1245762a779e5ee8431f53711333b9631af2e48',1,'44 Theobalds Road, WC1X 8NW',51.521431,-0.1135679);
INSERT INTO "locations" VALUES(2,'Angel Food Bakery','Specialist cupcake store with a made-to-order service, plus gluten-free options and classes.','dcf0a73e552ab682182236cab18e3490e17fdb26',1,'20 Meeting House Ln, Brighton BN1 1HB, United Kingdom',50.822242,-0.1408279);
INSERT INTO "ratings" VALUES(1,4,1);
INSERT INTO "ratings" VALUES(2,4,1);
INSERT INTO "tags" VALUES(1,'bakery',1);
INSERT INTO "tags" VALUES(2,' london',1);
INSERT INTO "tags" VALUES(3,' england',1);
INSERT INTO "tags" VALUES(4,'bakery',2);
INSERT INTO "tags" VALUES(5,' brighton',2);
INSERT INTO "tags" VALUES(6,' england',2);
INSERT INTO "users" VALUES(1,'RhiannonJane','12345678',NULL,'rhiannon@rhiannon.com','Rhiannon','Pauling');
