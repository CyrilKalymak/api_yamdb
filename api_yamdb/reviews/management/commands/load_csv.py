import sqlite3
import csv
import io

# from django.core.management import BaseCommand

# class Command(BaseCommand):
#     """Класс загрузки тестовой базы данных."""

tuples1 = []
with io.open('static/data/category.csv', 'r', encoding='utf-8', errors='ignore') as f:
    read_csv = csv.reader(f, delimiter=',')
    index = 0
    for row in read_csv:
        if index > 0:
            row = tuple(row)
            tuples1.append(row)
        index += 1
category = tuple(tuples1)

tuples2 = []
with io.open('static/data/comments.csv', 'r', encoding='utf-8', errors='ignore') as f:
    read_csv = csv.reader(f, delimiter=',')
    index = 0
    for row in read_csv:
        if index > 0:
            row = tuple(row)
            tuples2.append(row)
        index += 1
comments = tuple(tuples2)

tuples3 = []
with io.open('static/data/genre.csv', 'r', encoding='utf-8', errors='ignore') as f:
    read_csv = csv.reader(f, delimiter=',')
    index = 0
    for row in read_csv:
        if index > 0:
            row = tuple(row)
            tuples3.append(row)
        index += 1
genre = tuple(tuples3)

tuples4 = []
with io.open('static/data/review.csv', 'r', encoding='utf-8', errors='ignore') as f:
    read_csv = csv.reader(f, delimiter=',')
    index = 0
    for row in read_csv:
        if index > 0:
            row = tuple(row)
            tuples4.append(row)
        index += 1
review = tuple(tuples4)

tuples5 = []
with io.open('static/data/titles.csv', 'r', encoding='utf-8', errors='ignore') as f:
    read_csv = csv.reader(f, delimiter=',')
    index = 0
    for row in read_csv:
        if index > 0:
            row = tuple(row)
            tuples5.append(row)
        index += 1
titles = tuple(tuples5)

tuples6 = []
with io.open('static/data/users.csv', 'r', encoding='utf-8', errors='ignore') as f:
    read_csv = csv.reader(f, delimiter=',')
    index = 0
    for row in read_csv:
        if index > 0:
            row = tuple(row)
            tuples6.append(row)
        index += 1
users = tuple(tuples6)

tuples7 = []
with io.open('static/data/genre_title.csv', 'r', encoding='utf-8', errors='ignore') as f:
    read_csv = csv.reader(f, delimiter=',')
    index = 0
    for row in read_csv:
        if index > 0:
            row = tuple(row)
            tuples7.append(row)
        index += 1
genre_title = tuple(tuples7)

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

# Готовим SQL-запросы.
cur.executescript('''
CREATE TABLE IF NOT EXISTS users_user(
    id INTEGER PRIMARY KEY,
    username TEXT,
    email CHAR,
    role CHAR,
    bio TEXT,
    first_name CHAR,
    last_name CHAR,
    password CHAR DEFAULT '',
    last_login CHAR DEFAULT '',
    is_superuser CHAR DEFAULT '',
    is_staff CHAR DEFAULT '',
    is_active CHAR DEFAULT '',
    date_joined DATETIME DEFAULT ''
);
CREATE TABLE IF NOT EXISTS reviews_category(
    id INTEGER PRIMARY KEY,
    name CHAR,
    slug CHAR
);
CREATE TABLE IF NOT EXISTS reviews_genre(
    id INTEGER PRIMARY KEY,
    name TEXT,
    slug TEXT
);
CREATE TABLE IF NOT EXISTS reviews_title(
    id INTEGER PRIMARY KEY,
    name CHAR,
    year INTEGER,
    category_id INTEGER,
    description TEXT DEFAULT '',
    FOREIGN KEY(category_id) REFERENCES reviews_category(id)
);
CREATE TABLE IF NOT EXISTS reviews_review(
    id INTEGER PRIMARY KEY,
    text TEXT,
    author INTEGER,
    score INTEGER,
    pub_date DATETIME,
    title_id INTEGER,
    FOREIGN KEY(author) REFERENCES users_user(id),
    FOREIGN KEY(title_id) REFERENCES reviews_title(id)
);
CREATE TABLE IF NOT EXISTS reviews_comment(
    id INTEGER PRIMARY KEY,
    review_id INTEGER,
    text TEXT UNIQUE,
    author INTEGER,
    pub_date DATETIME,
    FOREIGN KEY(author) REFERENCES users_user(id),
    FOREIGN KEY(review_id) REFERENCES reviews_review(id)
);
CREATE TABLE IF NOT EXISTS reviews_genretitle(
    id INTEGER PRIMARY KEY,
    title_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY(title_id) REFERENCES reviews_title(id),
    FOREIGN KEY(genre_id) REFERENCES reviews_genre(id)
);
''')

cur.executemany('INSERT INTO reviews_category VALUES(?, ?, ?);', category)
cur.executemany('INSERT INTO reviews_comment VALUES(?, ?, ?, ?, ?);', comments)
cur.executemany('INSERT INTO reviews_genretitle VALUES(?, ?, ?);', genre_title)
cur.executemany('INSERT INTO reviews_genre VALUES(?, ?, ?);', genre)
cur.executemany('INSERT INTO reviews_review VALUES(?, ?, ?, ?, ?, ?);', review)
cur.executemany('INSERT INTO reviews_title VALUES(?, ?, ?, ?, "");', titles)
cur.executemany(
    'INSERT INTO users_user VALUES(?, ?, ?, ?, ?, ?, ?, "", "", "", "", "", "");',
    users
)

con.commit()
con.close()
