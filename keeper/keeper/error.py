class KeeperError(Exception):
    pass


class KeeperSocketError(KeeperError):
    pass


class KeeperSocketClosedError(KeeperSocketError):
    pass


# Ошибки возникающие при формировании фрейма
class KeeperFrameError(KeeperError):
    pass


class KeeperFrameTypeError(KeeperError):
    pass


class KeeperFrameStructureError(KeeperFrameError):
    pass


class KeeperVehicleError(KeeperError):
    pass


class KeeperVehicleRegistrationError(KeeperVehicleError):
    pass


# Ошибки возникающие при работе с бекэндами
class KeeperBackendError(KeeperError):
    pass


class KeeperBackendConnectionError(KeeperBackendError):
    pass


class KeeperBackendLoadDataError(KeeperBackendError):
    pass


class KeeperBackendReloadDataError(KeeperBackendError):
    pass


class KeeperBackendFatalError(KeeperError):
    pass



class KeeperVehicleRouteDetectError(KeeperVehicleError):
    pass


class KeeperVehicleRouteDetectRetriesError(KeeperVehicleRouteDetectError):
    pass


class KeeperVehicleRouteDetectLostError(KeeperVehicleRouteDetectError):
    pass


class KeeperVehicleRouteError(KeeperVehicleError):
    pass


class KeeperVehicleSpeedError(KeeperVehicleError):
    pass