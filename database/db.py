from configparser import ConfigParser

import psycopg2
from psycopg2.extras import DictCursor


class dbclient:
    def __init__(self, host, database, port, user, password):

        self.config = self.load_config()
        self.conn = self.connect(self.config)

    @staticmethod
    def connect(config):
        """ Connect to the PostgreSQL database server """
        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(**config) as conn:
                print('Connected to the PostgreSQL server.')
                return conn
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

    def disconnect(self):
        self.conn.close()

    @staticmethod
    def load_config(filename='database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)

        # get section, default to postgresql
        config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return config

    def query(self, query, parameters=None):
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(query, parameters)
                if cursor.description is not None:
                    return cursor.fetchall()


if __name__ == '__main__':
    client = dbclient('92.222.10.112', 'odoo_camajora_staging', '5432', 'camajora_staging',
                      'nufhvjdsoQRSBDFGfsduih6954i')
    print(client.query(
        "SELECT id,name, currency_id, code, deprecated, user_type_id, internal_type, internal_group, last_time_entries_checked, reconcile, "
        "note, company_id, group_id, create_uid, create_date, write_uid, write_date FROM public.account_account"))

    client.disconnect()
