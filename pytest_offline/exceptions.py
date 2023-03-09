class BlockedConnectionError(Exception):
    pass


class BlockedHostError(BlockedConnectionError):
    pass


class BlockedPortError(BlockedConnectionError):
    pass
