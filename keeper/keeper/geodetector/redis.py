import psycopg2
import redis
from keeper import error


class Detector:
    def __init__(self, location: str, rradius: int, pradius: int, runit: str = 'm', punit: str = 'm',
                 host: str = 'localhost', port: int = 6379, password: str = None, db: int = 0, gbdshost: str = None,
                 gbdsport: int = None, gbdsuser: str = None, gbdspass: str = None, gbdsdb: str = None):
        """Геодетектор с бекэндом в redis"""
        self.location = location
        self.rradius = rradius
        self.pradius = pradius
        self.runit = runit
        self.punit = punit

        # Geodetector backend
        self._dbh = None
        self.host = host
        self.port = port
        self.password = password
        self.dbx = db

        # Geodetector data source
        self.gbdshost = gbdshost
        self.gbdsport = gbdsport
        self.gbdsuser = gbdsuser
        self.gbdspass = gbdspass
        self.gbdsdb = gbdsdb

    def connect(self):
        try:
            self._dbh = redis.Redis(host=self.host,
                                    port=self.port,
                                    db=self.dbx,
                                    password=self.password)

        except Exception as e:
            raise error.KeeperBackendConnectionError(e)

    def load_geodata(self):
        # return None

        # todo зхагрузка геоданных с базы источника
        conn = None
        cursor = None

        try:
            conn = psycopg2.connect(dbname=self.gbdsdb,
                                    user=self.gbdsuser,
                                    password=self.gbdspass,
                                    host=self.gbdshost,
                                    port=self.gbdsport)

            cursor = conn.cursor()
        except redis.exceptions.ConnectionError as e:
            raise error.KeeperBackendLoadDataError(e)
        finally:
            cursor.close()
            conn.close()

    def reload_geodata(self, force=False):
        # todo перезагрузка геоданных из базы источника
        pass

    def georadius(self, longitude, latitude):
        geospatial = [longitude, latitude]

        route_points = [tuple(p.decode().split("_")) for p in self._dbh.georadius(f"{self.location}_route",
                                                                                  *geospatial,
                                                                                  self.rradius,
                                                                                  self.runit)]

        platform_points = [tuple(p.decode().split("_")) for p in self._dbh.georadius(f"{self.location}_platform",
                                                                                     *geospatial,
                                                                                     self.pradius,
                                                                                     self.punit)]

        return route_points, platform_points
