from . import redis, postgresql
import keeper.errors as error


def get_geodetector(params):
    if params.geobackend == 'redis':
        geodetector = redis.Detector(params.location, params.rradius, params.pradius, params.runit,
                                     params.punit, params.gbhost, params.gbport, params.gbdb)

        try:
            geodetector.connect()
            geodetector.load_geodata()
            # todo additionl actions
        except redis.exceptions.ConnectionError as e:
            raise error.KeeperBackendConnectionError(e)

        return geodetector

    elif params.geobackend == 'postgresql':
        raise NotImplementedError

    else:
        raise ValueError(f"Unknown geobackend '{params.geobackend}'")
