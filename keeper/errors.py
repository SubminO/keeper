class KeeperError(Exception):
    pass


class KeeperSocketError(KeeperError):
    pass


class KeeperSocketClosedError(KeeperSocketError):
    pass


class KeeperFrameError(KeeperError):
    pass


class KeeperFrameStructureError(KeeperFrameError):
    pass


class KeeperVehicleError(KeeperError):
    pass


class KeeperVehicleRegistrationError(KeeperVehicleError):
    pass