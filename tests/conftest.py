import pytest
import socket
from dcs_jupyter.connection import DCSConnection


@pytest.fixture
def dcs_connection():
    """
    Fixture that provides a DCSConnection instance.
    Skips tests if DCS is not running or connection fails.
    """
    try:
        with DCSConnection() as connection:
            connection.execute("return true")
            yield connection
    except socket.timeout:
        pytest.skip("DCS not running")
    except ConnectionError:
        pytest.skip("Failed to connect to DCS")
    except Exception as e:
        pytest.fail(f"Unexpected error during DCS connection: {e}")
