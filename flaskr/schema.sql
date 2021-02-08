DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS movements;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL);

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
    );



CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    productName TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES user (id)
    );

CREATE TABLE location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    locationName INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES user (id)
    );

CREATE TABLE movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    from_location INTEGER NOT NULL,
    to_location INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    qty INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (from_location) REFERENCES location (id)
    FOREIGN KEY (to_location) REFERENCES location (id)
    FOREIGN KEY (product_id) REFERENCES product (id)
    FOREIGN KEY (author_id) REFERENCES user (id)
    );

-- Sample data
INSERT INTO user
(username, password)
VALUES ('admin', 'pbkdf2:sha256:150000$0vDVUg7v$5b250b393375d1bd86288f19a07c2e515afe29f1f94e52e36c21d575906a173f');

INSERT INTO product
(author_id, productName)
VALUES (1,'product 1'),
  (1,'product 2'),
  (1,'product 3'),
  (1,'product 4');

INSERT INTO location
(author_id, locationName)
VALUES (1, 'City'),
  (1, 'Sharq'),
  (1, 'Salmiya'),
  (1, 'Mars');

INSERT INTO movements
(author_id, from_location, to_location, product_id, qty)
VALUES (1,0,1,1,23);
