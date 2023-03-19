import sqlite3
import csv

tuples1 = []
with open('category.csv', 'r') as f:
    read_csv = csv.reader(f, delimiter=',')
    for row in read_csv:
        row = tuple(row)
        tuples1.append(row)
category = tuple(tuples1)

tuples2 = []
with open('comments.csv', 'r') as f:
    read_csv = csv.reader(f, delimiter=',')
    for row in read_csv:
        row = tuple(row)
        tuples2.append(row)
comments = tuple(tuples2)

tuples3 = []
with open('genre.csv', 'r') as f:
    read_csv = csv.reader(f, delimiter=',')
    for row in read_csv:
        row = tuple(row)
        tuples3.append(row)
genre = tuple(tuples3)

tuples4 = []
with open('review.csv', 'r') as f:
    read_csv = csv.reader(f, delimiter=',')
    for row in read_csv:
        row = tuple(row)
        tuples4.append(row)
review = tuple(tuples4)

tuples5 = []
with open('titles.csv', 'r') as f:
    read_csv = csv.reader(f, delimiter=',')
    for row in read_csv:
        row = tuple(row)
        tuples5.append(row)
titles = tuple(tuples5)

tuples6 = []
with open('users.csv', 'r') as f:
    read_csv = csv.reader(f, delimiter=',')
    for row in read_csv:
        row = tuple(row)
        tuples6.append(row)
users = tuple(tuples6)

tuples7 = []
with open('genre_title.csv', 'r') as f:
    read_csv = csv.reader(f, delimiter=',')
    for row in read_csv:
        row = tuple(row)
        tuples7.append(row)
genre_title = tuple(tuples7)


con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Готовим SQL-запросы.
cur.executescript('''
CREATE TABLE IF NOT EXISTS reviews_Category(
    id INTEGER PRIMARY KEY,
    name CHAR,
    slug CHAR
);

CREATE TABLE IF NOT EXISTS reviews_Comment(
    id INTEGER PRIMARY KEY,
    review_id INTEGER FOREIGN KEY,
    text TEXT,
    author INTEGER FOREIGN KEY,
    pub_date DATETIME
);
CREATE TABLE IF NOT EXISTS reviews_GenreTitle(
    id INTEGER PRIMARY KEY,
    title_id INTEGER FOREIGN KEY,
    genre_id INTEGER FOREIGN KEY
);
CREATE TABLE IF NOT EXISTS reviews_Genre(
    id INTEGER PRIMARY KEY,
    name TEXT,
    slug TEXT
);
CREATE TABLE IF NOT EXISTS reviews_Review(
    id INTEGER PRIMARY KEY,
    title_id INTEGER FOREIGN KEY,
    text TEXT,
    author INTEGER FOREIGN KEY,
    score INTEGER,
    pub_date DATETIME
);
CREATE TABLE IF NOT EXISTS reviews_Title(
    id INTEGER PRIMARY KEY,
    name CHAR,
    year INTEGER,
    category INTEGER FOREIGN KEY
);
CREATE TABLE IF NOT EXISTS users_User(
    id INTEGER PRIMARY KEY,
    username TEXT,
    email CHAR,
    role CHAR,
    bio TEXT,
    first_name CHAR,
    last_name CHAR
);
''');

cur.executemany('INSERT INTO reviews_Category VALUES(?, ?, ?);', category)
cur.executemany('INSERT INTO reviews_Comment VALUES(?, ?, ?, ?, ?);', comments)
cur.executemany('INSERT INTO reviews_GenreTitle VALUES(?, ?, ?);', genre_title)
cur.executemany('INSERT INTO reviews_Genre VALUES(?, ?, ?);', genre)
cur.executemany('INSERT INTO reviews_Review VALUES(?, ?, ?, ?, ?, ?);', review)
cur.executemany('INSERT INTO reviews_Title VALUES(?, ?, ?, ?);', titles)
cur.executemany('INSERT INTO users_User VALUES(?, ?, ?, ?, ?, ?, ?);', users)


con.commit()
con.close()