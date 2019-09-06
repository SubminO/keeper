from keeper.geodetector import redis, postgresql
from keeper import error


def get_geodetector(params):
    if params.geobackend == 'redis':
        geodetector = redis.Detector(params.location, params.rradius, params.pradius,
                                     params.runit, params.punit, params.gbhost,
                                     params.gbport, params.gbpass, params.gbdb,
                                     params.gbdshost, params.gbdsport, params.gbdsuser,
                                     params.gbdspass, params.gbdsdb)

        try:
            geodetector.connect()
            geodetector.load_geodata()
        except error.KeeperBackendConnectionError as e:
            raise error.KeeperBackendFatalError(e)
        except error.KeeperBackendLoadDataError as e:
            raise error.KeeperBackendFatalError(e)

        return geodetector

    elif params.geobackend == 'postgresql':
        raise NotImplementedError

    else:
        raise error.KeeperBackendError(f"Unknown geobackend '{params.geobackend}'")
