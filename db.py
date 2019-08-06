import sqlite3
from contextlib import closing
from datetime import datetime, timedelta, date


db_path = 'db/temperate.db'


def connect(db=db_path):
    return setup_db(sqlite3.connect(db, check_same_thread=False))


def tables_exist(conn):
    with closing(conn.cursor()) as cursor:
        cursor.execute("select count(*) from sqlite_master where type='table' and name='parameter'")
        return bool(cursor.fetchone()[0])


def create_tables(conn):
    with closing(conn.cursor()) as cursor:
        cursor.execute('create table parameter (name text not null primary key, value text not null)')
        cursor.execute('create table measurement (id integer primary key, timestamp integer not null, name text not null, value real not null)')
        cursor.execute('create index measurement_timestamp_idx on measurement (timestamp)')


def setup_db(conn):
    if not tables_exist(conn):
        create_tables(conn)
    return conn


def query(conn, query):
    with closing(conn.cursor()) as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def set_parameter(conn, name, value):
    with conn:
        conn.execute('replace into parameter (name, value) values (?, ?)', (name, value))


def get_parameter(conn, name, type_: type = str):
    with closing(conn.cursor()) as cursor:
        cursor.execute('select value from parameter where name = ?', (name, ))
        result = cursor.fetchone()
        if result:
            return type_(result[0])
        return None


def add_measurement(conn, name, value, timestamp=None):
    if not timestamp:
        timestamp = datetime.now()
    with conn:
        conn.execute('insert into measurement (timestamp, name, value) values (?, ?, ?)',
                     (int(timestamp.timestamp()), name, value))


def get_measurements(conn, day=None):
    if not day:
        day = date.today()
    today = datetime(day.year, day.month, day.day)
    tomorrow = today + timedelta(days=1)

    with closing(conn.cursor()) as cursor:
        cursor.execute('select timestamp, name, value from measurement where timestamp >= ? and timestamp < ? order by timestamp asc',
                       (int(today.timestamp()), int(tomorrow.timestamp())))
        result = cursor.fetchall()
        return [(datetime.fromtimestamp(row[0]), row[1], row[2]) for row in result]


def get_recent_measurements(conn, days_back=5):
    result = []
    for n in range(days_back):
        day = (datetime.now() - timedelta(days=n)).date()
        measurements = get_measurements(conn, day)
        if measurements:
            result.append((day, measurements))
    return result


if __name__ == '__main__':
    print('connecting to', db_path)
    conn = connect()

    while True:
        try:
            rows = query(conn, input())
            if len(rows):
                for row in rows:
                    print(row)
            else:
                print('no results')
        except sqlite3.DatabaseError as db_error:
            print(db_error)
        except (KeyboardInterrupt, EOFError):
            break
    conn.close()

