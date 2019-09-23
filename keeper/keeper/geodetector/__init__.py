from math import sin, cos, sqrt, atan2, radians

from keeper.geodetector import redis, postgresql
from keeper import error
from keeper.settings import *


def get_geodetector(params, backend):
    if params.geobackend == 'redis':
        geodetector = redis.Detector(params, backend.dbsrc)

        try:
            geodetector.connect()
            geodetector.reload_geodata(force=True)
        except error.KeeperBackendConnectionError as e:
            raise error.KeeperBackendFatalError(e)
        except error.KeeperBackendLoadDataError as e:
            raise error.KeeperBackendFatalError(e)

        return geodetector

    elif params.geobackend == 'postgresql':
        raise NotImplementedError

    else:
        raise error.KeeperBackendError(f"Unknown geobackend '{params.geobackend}'")


def get_distance(prev_geospatial, cur_geospatial):
    lon1, lat1 = prev_geospatial
    lon2, lat2 = cur_geospatial

    dlon, dlat = radians(lon2 - lon1), radians(lat2 - lat1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2

    return EARTH_RADIUS * 2 * atan2(sqrt(a), sqrt(1 - a))
