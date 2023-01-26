import os
import logging
import sqlite3
from dataclasses import asdict
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection
from dotenv import load_dotenv

from movie_classes import (
    Genre, GenreFilmWork, PersonFilmWork, Person, FilmWork
)

load_dotenv()

logging.basicConfig(
    format=os.environ.get('LOG_FORMAT'),
    level=os.environ.get('LOG_LEVEL'),
    filename='%s.log' % os.environ.get('APP_NAME')
)
logger = logging.getLogger(os.environ.get('APP_NAME'))


DSL = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASS'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432),
        'options': '-c search_path=content',
    }

TABLE_CLASSES = {
    'genre': Genre,
    'genre_film_work': GenreFilmWork,
    'person_film_work': PersonFilmWork,
    'person': Person,
    'film_work': FilmWork
}


class SQLiteExtractor:
    def __init__(self, conn: sqlite3.Connection):
        self.curs = conn.cursor()
        self.data = {
            'genre': [],
            'genre_film_work': [],
            'person_film_work': [],
            'person': [],
            'film_work': []
        }

    def extract_movies(self):
        try:
            tables = [x[0] for x in self.curs.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            ).fetchall()]
            for table in tables:
                raw_data = self.curs.execute(
                    f'SELECT * FROM {table};'
                ).fetchall()
                for item in raw_data:
                    self.data[table].append(
                        asdict(TABLE_CLASSES[table](**item))
                    )

            self.curs.close()
            return self.data
        except sqlite3.Error as err:
            logger.error(err)
            return


class PostgresSaver:
    def __init__(self, conn: _connection):
        self.curs = conn.cursor()

    def save_all_data(self, data: dict):
        try:
            tables = [i for i in data.keys()]
            for table in tables:
                for items in data[table]:
                    keys = ', '.join([str(x) for x in items.keys()])
                    s = f"{'%s, ' * (len(items.values()) - 1) + '%s'}"

                    self.curs.execute(
                        f'INSERT INTO content.{table} ({keys}) VALUES ({s});',
                        tuple(list(items.values()))
                    )
        except psycopg2.Error as err:
            logger.error(err)
            return


@contextmanager
def sqlite_conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def load_from_sqlite(
        connection: sqlite3.Connection,
        pg_connection: _connection
):
    postgres_saver = PostgresSaver(pg_connection)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    with sqlite_conn_context(os.environ.get('DB_PATH')) as sqlite_conn,\
            psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
