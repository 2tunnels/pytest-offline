import socket

import pytest

from pytest_offline.exceptions import BlockedHostError, BlockedPortError
from pytest_offline.utils import block_hosts, block_ports


@pytest.mark.parametrize("family,host", [(socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::1")])
def test_block_hosts_ip_connect(family: int, host: str) -> None:
    # Default behaviour
    with socket.socket(family, socket.SOCK_STREAM) as s, pytest.raises(ConnectionRefusedError):
        s.connect((host, 8000))

    # Host is blocked
    with (
        socket.socket(family, socket.SOCK_STREAM) as s,
        pytest.raises(BlockedHostError) as exc_info,
        block_hosts(host),
    ):
        s.connect((host, 8000))

    assert repr(exc_info.value) == f"BlockedHostError('{host}:8000 connection was blocked')"

    # Connection to non-blocked host
    with (
        socket.socket(family, socket.SOCK_STREAM) as s,
        pytest.raises(ConnectionRefusedError),
        block_hosts("1.1.1.1"),
    ):
        s.connect((host, 8000))

    # Back to default behaviour
    with socket.socket(family, socket.SOCK_STREAM) as s, pytest.raises(ConnectionRefusedError):
        s.connect((host, 8000))


@pytest.mark.parametrize("family,host", [(socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::1")])
def test_block_hosts_ip_connect_ex(family: int, host: str) -> None:
    # Default behaviour
    with socket.socket(family, socket.SOCK_STREAM) as s:
        assert s.connect_ex((host, 8000)) != 0

    # Host is blocked
    with (
        socket.socket(family, socket.SOCK_STREAM) as s,
        pytest.raises(BlockedHostError) as exc_info,
        block_hosts(host),
    ):
        s.connect_ex((host, 8000))

    assert repr(exc_info.value) == f"BlockedHostError('{host}:8000 connection was blocked')"

    # Connection to non-blocked host
    with socket.socket(family, socket.SOCK_STREAM) as s, block_hosts("1.1.1.1"):
        assert s.connect_ex((host, 8000)) != 0

    # Back to default behaviour
    with socket.socket(family, socket.SOCK_STREAM) as s:
        assert s.connect_ex((host, 8000)) != 0


def test_block_hosts_hostname_connect():
    # Default behaviour
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, pytest.raises(socket.gaierror):
        s.connect(("foo.bar", 80))

    # Host is blocked
    with (
        socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s,
        pytest.raises(BlockedHostError) as exc_info,
        block_hosts("foo.bar"),
    ):
        s.connect(("foo.bar", 80))

    assert repr(exc_info.value) == "BlockedHostError('foo.bar:80 connection was blocked')"

    # Connection to non-blocked host
    with (
        socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s,
        pytest.raises(socket.gaierror),
        block_hosts("example.com"),
    ):
        s.connect(("foo.bar", 80))

    # Back to default behaviour
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, pytest.raises(socket.gaierror):
        s.connect(("foo.bar", 80))


def test_block_hosts_hostname_connect_ex():
    # Default behaviour
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, pytest.raises(socket.gaierror):
        assert s.connect_ex(("foo.bar", 80)) != 0

    # Host is blocked
    with (
        socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s,
        pytest.raises(BlockedHostError) as exc_info,
        block_hosts("foo.bar"),
    ):
        s.connect_ex(("foo.bar", 80))

    assert repr(exc_info.value) == "BlockedHostError('foo.bar:80 connection was blocked')"

    # Connection to non-blocked host
    with (
        socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s,
        pytest.raises(socket.gaierror),
        block_hosts("example.com"),
    ):
        s.connect_ex(("foo.bar", 80))

    # Back to default behaviour
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, pytest.raises(socket.gaierror):
        s.connect(("foo.bar", 80))


@pytest.mark.parametrize("family,host", [(socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::1")])
def test_block_ports_connect(family: int, host: str) -> None:
    # Default behaviour
    with socket.socket(family, socket.SOCK_STREAM) as s, pytest.raises(ConnectionRefusedError):
        s.connect((host, 8000))

    # Port is blocked
    with (
        socket.socket(family, socket.SOCK_STREAM) as s,
        pytest.raises(BlockedPortError) as exc_info,
        block_ports(8000),
    ):
        s.connect((host, 8000))

    assert repr(exc_info.value) == f"BlockedPortError('{host}:8000 connection was blocked')"

    # Connection to non-blocked port
    with (
        socket.socket(family, socket.SOCK_STREAM) as s,
        pytest.raises(ConnectionRefusedError),
        block_ports(9000),
    ):
        s.connect((host, 8000))

    # Back to default behaviour
    with socket.socket(family, socket.SOCK_STREAM) as s, pytest.raises(ConnectionRefusedError):
        s.connect((host, 8000))


@pytest.mark.parametrize("family,host", [(socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::1")])
def test_block_ports_connect_ex(family: int, host: str) -> None:
    # Default behaviour
    with socket.socket(family, socket.SOCK_STREAM) as s:
        assert s.connect_ex((host, 8000)) != 0

    # Port is blocked
    with (
        socket.socket(family, socket.SOCK_STREAM) as s,
        pytest.raises(BlockedPortError) as exc_info,
        block_ports(8000),
    ):
        s.connect_ex((host, 8000))

    assert repr(exc_info.value) == f"BlockedPortError('{host}:8000 connection was blocked')"

    # Connection to non-blocked port
    with socket.socket(family, socket.SOCK_STREAM) as s, block_ports(9000):
        assert s.connect_ex((host, 8000)) != 0

    # Back to default behaviour
    with socket.socket(family, socket.SOCK_STREAM) as s:
        assert s.connect_ex((host, 8000)) != 0
