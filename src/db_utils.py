import mariadb
import sys
import datetime
import argparse
import json
from pyjavaproperties import Properties

conn = None
cursor = None


def close_connection():
    conn.close()


def open_connection():
    global conn
    global cursor

    p = load_properties()

    try:
        conn = mariadb.connect(
            user=p['datasource.user'],
            password=p['datasource.password'],
            host=p['datasource.host'],
            port=int(p['datasource.port']),
            database=p['datasource.database']

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    cursor = conn.cursor()


def load_properties():
    p = Properties()
    p.load(open('application.properties'))

    return p


def add_all(values):
    open_connection()

    for value in values:
        now = datetime.datetime.now()
        cursor.execute(
            "INSERT INTO frames (value, created_at) VALUES ( ?, ?)",
            (str(value), now))

    close_connection()


def add_new(value):
    open_connection()

    now = datetime.datetime.now()

    cursor.execute(
        "INSERT INTO frames (value, created_at) VALUES ( ?, ?)",
        (str(value), now))

    close_connection()


def get_top(top, order):
    open_connection()

    order = 'DESC' if order != 'DESC' and order != 'ASC' else order

    cursor.execute(
        "SELECT * FROM frames ORDER BY created_at {} LIMIT {}".format(order, top)
    )

    read()
    close_connection()


def get_all():
    open_connection()

    cursor.execute(
        "SELECT * FROM frames"
    )

    read()
    close_connection()


def read():
    frame_list = []

    for (id, value, created_at) in cursor:
        frame_list.append({'id': id, 'value': value, 'created_at': str(created_at)})

    print(json.dumps(frame_list, indent=4, sort_keys=False))


def main():
    parser = argparse.ArgumentParser(description='Available options:')
    parser.add_argument('-l', '--limit', type=int,
                        help='Limit results ex. -l 10')

    parser.add_argument('-o', '--order', type=str,
                        help='Order DESC or ASC')

    args = parser.parse_args()

    if args.limit is None:
        get_all()
    else:
        limit = args.limit
        order = args.order
        get_top(int(limit), "DESC" if order is None else order)


if __name__ == "__main__":
    main()
