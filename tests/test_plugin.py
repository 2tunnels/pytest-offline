from _pytest.pytester import Pytester

_tests = """
import socket
        
import pytest

def test_block_hosts_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, pytest.raises(ConnectionRefusedError):
        assert s.connect(("127.0.0.1", 8000))

def test_block_hosts_hostname():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, pytest.raises(ConnectionRefusedError):
        assert s.connect(("localhost", 8000))

def test_block_ports_8000():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, pytest.raises(ConnectionRefusedError):
        assert s.connect(("127.0.0.1", 8000))

def test_block_ports_8001():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, pytest.raises(ConnectionRefusedError):
        assert s.connect(("127.0.0.1", 8001))
"""


def test_default_behaviour_without_options(pytester: Pytester):
    pytester.makepyfile(_tests)

    result = pytester.runpytest()

    result.assert_outcomes(passed=4)


def test_default_behaviour_with_options(pytester: Pytester):
    pytester.makepyfile(_tests)

    result = pytester.runpytest("--block-host", "example.com", "--block-port", "443")

    result.assert_outcomes(passed=4)


def test_block_hosts_ip(pytester: Pytester):
    pytester.makepyfile(_tests)

    result = pytester.runpytest("--block-host", "127.0.0.1")

    result.assert_outcomes(passed=1, failed=3)


def test_block_hosts_hostname(pytester: Pytester):
    pytester.makepyfile(_tests)

    result = pytester.runpytest("--block-host", "localhost")

    result.assert_outcomes(passed=3, failed=1)


def test_block_hosts_all(pytester: Pytester):
    pytester.makepyfile(_tests)

    result = pytester.runpytest("--block-host", "127.0.0.1", "--block-host", "localhost")

    result.assert_outcomes(failed=4)


def test_block_ports_8000(pytester: Pytester):
    pytester.makepyfile(_tests)

    result = pytester.runpytest("--block-port", "8000")

    result.assert_outcomes(passed=1, failed=3)


def test_block_ports_8001(pytester: Pytester):
    pytester.makepyfile(_tests)

    result = pytester.runpytest("--block-port", "8001")

    result.assert_outcomes(passed=3, failed=1)


def test_block_ports_all(pytester: Pytester):
    pytester.makepyfile(_tests)

    result = pytester.runpytest("--block-port", "8000", "--block-port", "8001")

    result.assert_outcomes(failed=4)
