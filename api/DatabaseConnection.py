import traceback

import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    def __init__(self, database_settings):
        self.__host = database_settings["host"]
        self.__port = database_settings["port"]
        self.__database = database_settings["databaseName"]
        self.__user = database_settings["user"]
        self.__password = database_settings["password"]

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
