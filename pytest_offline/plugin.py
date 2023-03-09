from typing import Iterator, Optional

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest

from pytest_offline.utils import block_hosts, block_ports


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--block-host",
        action="append",
        dest="blocked_hosts",
    )
    parser.addoption(
        "--block-port",
        action="append",
        dest="blocked_ports",
    )


@pytest.fixture(autouse=True)
def _block_hosts(request: SubRequest) -> Iterator[None]:
    blocked_hosts: Optional[list[str]] = request.config.getoption("blocked_hosts")

    if blocked_hosts:
        with block_hosts(*blocked_hosts):
            yield
    else:
        yield


@pytest.fixture(autouse=True)
def _block_ports(request: SubRequest) -> Iterator[None]:
    blocked_ports: Optional[list[str]] = request.config.getoption("blocked_ports")

    if blocked_ports is None:
        yield
        return

    integers = [int(blocked_port) for blocked_port in blocked_ports]

    with block_ports(*integers):
        yield
