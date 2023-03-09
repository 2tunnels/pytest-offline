import socket
from contextlib import contextmanager
from functools import wraps
from typing import Iterator, Optional
from unittest.mock import patch

from pytest_offline.exceptions import BlockedHostError, BlockedPortError


def _block_connection(*, hosts: Optional[tuple[str]] = None, ports: Optional[tuple[int]] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(self: socket.socket, address: tuple[str, int]):
            host = address[0]
            port = address[1]

            if hosts is not None and host in hosts:
                raise BlockedHostError(f"{host}:{port} connection was blocked")

            if ports is not None and port in ports:
                raise BlockedPortError(f"{host}:{port} connection was blocked")

            return func(self, address)

        return wrapper

    return decorator


@contextmanager
def block_hosts(*hosts: str) -> Iterator[None]:
    with (
        patch.object(socket.socket, "connect", new=_block_connection(hosts=hosts)(socket.socket.connect)),
        patch.object(socket.socket, "connect_ex", new=_block_connection(hosts=hosts)(socket.socket.connect_ex)),
    ):
        yield


@contextmanager
def block_ports(*ports: int) -> Iterator[None]:
    with (
        patch.object(socket.socket, "connect", new=_block_connection(ports=ports)(socket.socket.connect)),
        patch.object(socket.socket, "connect_ex", new=_block_connection(ports=ports)(socket.socket.connect_ex)),
    ):
        yield
