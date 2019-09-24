from geographiclib.geodesic import Geodesic

from keeper.geodetector import redis, postgresql
from keeper import error


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
    geod = Geodesic.WGS84
    g = geod.Inverse(*prev_geospatial, *cur_geospatial, outmask=Geodesic.DISTANCE)

    return g['s12'] / 1000
