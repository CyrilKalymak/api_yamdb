# import sqlite3
# import csv
# import io

# tuples1 = []
# with io.open('static/data/category.csv', 'r', encoding='utf-8', errors='ignore') as f:
#     read_csv = csv.reader(f, delimiter=',')
#     for row in read_csv:
#         row = tuple(row)
#         tuples1.append(row)
# category = tuple(tuples1)

# tuples2 = []
# with io.open('static/data/comments.csv', 'r', encoding='utf-8', errors='ignore') as f:
#     read_csv = csv.reader(f, delimiter=',')
#     for row in read_csv:
#         row = tuple(row)
#         tuples2.append(row)
# comments = tuple(tuples2)

# tuples3 = []
# with io.open('static/data/genre.csv', 'r', encoding='utf-8', errors='ignore') as f:
#     read_csv = csv.reader(f, delimiter=',')
#     for row in read_csv:
#         row = tuple(row)
#         tuples3.append(row)
# genre = tuple(tuples3)

# tuples4 = []
# with io.open('static/data/review.csv', 'r', encoding='utf-8', errors='ignore') as f:
#     read_csv = csv.reader(f, delimiter=',')
#     for row in read_csv:
#         row = tuple(row)
#         tuples4.append(row)
# review = tuple(tuples4)

# tuples5 = []
# with io.open('static/data/titles.csv', 'r', encoding='utf-8', errors='ignore') as f:
#     read_csv = csv.reader(f, delimiter=',')
#     for row in read_csv:
#         row = tuple(row)
#         tuples5.append(row)
# titles = tuple(tuples5)

# tuples6 = []
# with io.open('static/data/users.csv', 'r', encoding='utf-8', errors='ignore') as f:
#     read_csv = csv.reader(f, delimiter=',')
#     for row in read_csv:
#         row = tuple(row)
#         tuples6.append(row)
# users = tuple(tuples6)

# tuples7 = []
# with io.open('static/data/genre_title.csv', 'r', encoding='utf-8', errors='ignore') as f:
#     read_csv = csv.reader(f, delimiter=',')
#     for row in read_csv:
#         row = tuple(row)
#         tuples7.append(row)
# genre_title = tuple(tuples7)


# con = sqlite3.connect('db.sqlite')
# cur = con.cursor()

# # Готовим SQL-запросы.
# cur.executescript('''
# CREATE TABLE IF NOT EXISTS users_user(
#     id INTEGER PRIMARY KEY,
#     username TEXT,
#     email CHAR,
#     role CHAR,
#     bio TEXT,
#     first_name CHAR,
#     last_name CHAR
# );
# CREATE TABLE IF NOT EXISTS reviews_category(
#     id INTEGER PRIMARY KEY,
#     name CHAR,
#     slug CHAR
# );
# CREATE TABLE IF NOT EXISTS reviews_genre(
#     id INTEGER PRIMARY KEY,
#     name TEXT,
#     slug TEXT
# );
# CREATE TABLE IF NOT EXISTS reviews_title(
#     id INTEGER PRIMARY KEY,
#     name CHAR,
#     year INTEGER,
#     category_id INTEGER,
#     FOREIGN KEY(category_id) REFERENCES reviews_category(id)
# );
# CREATE TABLE IF NOT EXISTS reviews_review(
#     id INTEGER PRIMARY KEY,
#     title_id INTEGER,
#     FOREIGN KEY(title_id) REFERENCES reviews_title(id),
#     "text" TEXT UNIQUE,
#     author INTEGER,
#     FOREIGN KEY(author) REFERENCES users_user(id),
#     score INTEGER,
#     pub_date DATETIME
# );
# CREATE TABLE IF NOT EXISTS reviews_comment(
#     id INTEGER PRIMARY KEY,
#     review_id INTEGER,
#     FOREIGN KEY(review_id) REFERENCES reviews_review(id),
#     text TEXT UNIQUE,
#     author INTEGER,
#     FOREIGN KEY(author) REFERENCES users_user(id),
#     pub_date DATETIME
# );
# CREATE TABLE IF NOT EXISTS reviews_genretitle(
#     id INTEGER PRIMARY KEY,
#     title_id INTEGER,
#     FOREIGN KEY(title_id) REFERENCES reviews_title(id),
#     genre_id INTEGER,
#     FOREIGN KEY(genre_id) REFERENCES reviews_genre(id)
# );
# ''')

# cur.executemany('INSERT INTO reviews_category VALUES(?, ?, ?);', category)
# cur.executemany('INSERT INTO reviews_comment VALUES(?, ?, ?, ?, ?);', comments)
# cur.executemany('INSERT INTO reviews_genretitle VALUES(?, ?, ?);', genre_title)
# cur.executemany('INSERT INTO reviews_genre VALUES(?, ?, ?);', genre)
# cur.executemany('INSERT INTO reviews_review VALUES(?, ?, ?, ?, ?, ?);', review)
# cur.executemany('INSERT INTO reviews_title VALUES(?, ?, ?, ?);', titles)
# cur.executemany('INSERT INTO users_user VALUES(?, ?, ?, ?, ?, ?, ?);', users)


# con.commit()
# con.close()

import csv
import os

from django.core.management import BaseCommand
from django.db import IntegrityError

from api_yamdb.settings import CSV_FILES_DIR
from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title
)
from api_yamdb.users.models import User

from django.core.management import call_command

FILES_CLASSES = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'users': User,
    'review': Review,
    'comments': Comment,
}

FIELDS = {
    'category': ('category', Category),
    'title_id': ('title', Title),
    'genre_id': ('genre', Genre),
    'author': ('author', User),
    'review_id': ('review', Review),
}


def open_csv_file(file_name):
    """Менеджер контекста для открытия csv-файлов."""
    csv_file = file_name + '.csv'
    csv_path = os.path.join(CSV_FILES_DIR, csv_file)
    try:
        with (open(csv_path, encoding='utf-8')) as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        print(f'Файл {csv_file} не найден.')
        return


def change_foreign_values(data_csv):
    """Изменяет значения."""
    data_csv_copy = data_csv.copy()
    for field_key, field_value in data_csv.items():
        if field_key in FIELDS.keys():
            field_key0 = FIELDS[field_key][0]
            data_csv_copy[field_key0] = FIELDS[field_key][1].objects.get(
                pk=field_value)
    return data_csv_copy


def load_csv(file_name, class_name):
    """Осуществляет загрузку csv-файлов."""
    table_not_loaded = f'Таблица {class_name.__qualname__} не загружена.'
    table_loaded = f'Таблица {class_name.__qualname__} загружена.'
    data = open_csv_file(file_name)
    rows = data[1:]
    for row in rows:
        data_csv = dict(zip(data[0], row))
        data_csv = change_foreign_values(data_csv)
        try:
            table = class_name(**data_csv)
            table.save()
        except (ValueError, IntegrityError) as error:
            print(f'Ошибка в загружаемых данных. {error}. '
                  f'{table_not_loaded}')
            break
    print(table_loaded)


class Command(BaseCommand):
    """Класс загрузки тестовой базы данных."""

    def handle(self, *args, **options):
        for key, value in FILES_CLASSES.items():
            print(f'Загрузка таблицы {value.__qualname__}')
            load_csv(key, value)
