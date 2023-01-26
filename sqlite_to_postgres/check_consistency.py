import os
from datetime import datetime, timezone
from dataclasses import asdict

import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

from load_data import sqlite_conn_context, TABLE_CLASSES, DSL

load_dotenv()


TABLES = [i for i in TABLE_CLASSES.keys()]


def test_integrity_and_tables():
    sqlite_rows, postgresql_rows = {}, {}
    with sqlite_conn_context(os.environ.get('DB_PATH')) as sqlite_conn,\
            psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
        sqlite_curs = sqlite_conn.cursor()
        postgresql_curs = pg_conn.cursor()
        for table in TABLES:
            sqlite_table_records = sqlite_curs.execute(
                f'SELECT * FROM {table};'
            ).fetchall()
            sqlite_rows[table] = len(sqlite_table_records)

            postgresql_curs.execute(
                f'SELECT COUNT(*) FROM content.{table}'
            )
            postgresql_rows[table] = postgresql_curs.fetchone()[0]

        sqlite_curs.close()

    assert [x for x in sqlite_rows.keys()] == \
           [x for x in postgresql_rows.keys()] == TABLES

    assert sqlite_rows == postgresql_rows


def test_content():
    sqlite_result = {
        'genre': [],
        'genre_film_work': [],
        'person_film_work': [],
        'person': [],
        'film_work': []
    }
    postgres_result = {
        'genre': [],
        'genre_film_work': [],
        'person_film_work': [],
        'person': [],
        'film_work': []
    }

    with sqlite_conn_context(os.environ.get('DB_PATH')) as sqlite_conn, \
            psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
        sqlite_curs = sqlite_conn.cursor()
        postgresql_curs = pg_conn.cursor()
        for table in TABLES:
            query = f'SELECT * FROM {table}'

            sqlite_data = sqlite_curs.execute(query).fetchall()
            for item in sqlite_data:
                sqlite_result[table].append(
                    asdict(TABLE_CLASSES[table](**item))
                )

            postgresql_curs.execute(query)
            postgres_data = postgresql_curs.fetchall()
            for item in postgres_data:
                postgres_result[table].append(
                    asdict(TABLE_CLASSES[table](**item))
                )

        for key, value in sqlite_result.items():
            for row in sqlite_result[key]:
                row['created_at'] = datetime.strptime(
                    row['created_at'], '%Y-%m-%d %H:%M:%S.%f+00'
                ).replace(tzinfo=timezone.utc)

                try:
                    row['updated_at'] = datetime.strptime(
                        row['updated_at'], '%Y-%m-%d %H:%M:%S.%f+00'
                    ).replace(tzinfo=timezone.utc)
                except KeyError:
                    continue

        sqlite_curs.close()

        assert sqlite_result == postgres_result
