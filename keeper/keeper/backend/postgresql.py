import psycopg2
from .. import error


class Postgresql:
    def __init__(self, params):
        self.host = params.dbshost
        self.port = params.dbsport
        self.user = params.dbsuser
        self.password = params.dbspass
        self.dbname = params.dbsdb

        self._conn = None
        self._cursor = None

    @property
    def cursor(self):
        # todo проверка на готовность соединения
        return self._cursor

    def connect(self):
        try:
            self._conn = psycopg2.connect(dbname=self.dbname,
                                          user=self.user,
                                          password=self.password,
                                          host=self.host,
                                          port=self.port)

            self._cursor = self._conn.cursor()
        except psycopg2.OperationalError as e:
            raise error.KeeperBackendConnectionError

    def desctroy(self):
        self._cursor.close()
        self._conn.close()
