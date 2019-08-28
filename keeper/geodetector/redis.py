import redis


class Detector:
    def __init__(self, location, rradius, pradius, runit: str='m', punit: str='m',
                 host: str='localhost', port: int=6379, db: int=0):
        # todo вынести всю бизнеслогику из инита. для примера см
        # https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_factory.htm
        self.location = location
        self.rradius = rradius
        self.pradius = pradius
        self.runit = runit
        self.punit = punit

        self._redis = None
        self.host = host
        self.port = port
        self.db = db

    def connect(self):
        self._redis = redis.Redis(host=self.host, port=self.port, db=self.db)
        self._redis.
        pass

    def load_geodata(self):
        # todo зхагрузка геоданных с базы источника
        pass

    def reload_geodata(self):
        # todo зхагрузка геоданных с базы источника
        pass

    def georadius(self, *args, **kwargs):
        return []