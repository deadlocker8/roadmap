import traceback

import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    def __init__(self, host, port, database, user, password):
        self.__host = host
        self.__port = port
        self.__database = database
        self.__user = user
        self.__password = password

    def __enter__(self):
        self.__connection = psycopg2.connect(user=self.__user,
                                             password=self.__password,
                                             host=self.__host,
                                             port=self.__port,
                                             database=self.__database)
        self.__cursor = self.__connection.cursor(cursor_factory=RealDictCursor)
        return self.__cursor

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

        if self.__connection:
            self.__cursor.close()
            self.__connection.close()

        return True
