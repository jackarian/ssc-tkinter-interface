import psycopg2 as pg
from psycopg2.extras import DictCursor


class dbclient:
    def __init__(self, host, database, port, user, password):
        self.connection = pg.connect()

    def query(self, query, parameters=None):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(query, parameters)
                if cursor.descriptions is not None:
                    return cursor.fetchall()


if __name__ == '__main__':
    client = dbclient()
