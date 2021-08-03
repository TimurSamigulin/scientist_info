from mysql.connector import connect
import mysql.connector

class Connector:
    db_config = dict(
        user='root',
        password='example',
        host='10.7.4.10',
        port=3306,
        database='exclusive'
    )

    def __init__(self, db_name, user, password, host, port):
        self.__db_name = db_name
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        # self.connection = mysql.connector.connect(**self.db_config)


    def insert_data(self, table_name, columns, values, ignore=False):
        if not len(values):
            return
        ignore = '' if not ignore else 'IGNORE'

        query = 'INSERT {} INTO {} ({}) VALUES {}'


        query = query.format(
            ignore,
            table_name,
            ', '.join(columns),
            values
        )

        lastid = self.__execute(query, fetch=False, commit=True)
        return lastid

    def __execute(self, query, fetch=False, commit=False):
        with connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                password=self.__password,
                database=self.__db_name
        ) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    result = cursor.fetchall() if fetch else None
                    if commit:
                        connection.commit()
                    lastid = cursor.lastrowid
                    return cursor.lastrowid
                except Exception as e:
                    raise e
