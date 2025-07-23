import pytest
import socket

try:
    from pydantic_ai.models.test import TestModel
    from pydantic_ai.tools import RunContext
    from pydantic_ai.usage import Usage
except ImportError:
    raise ImportError("PydanticAI is required for agent functionality. Install with: pip install 'dcs-jupyter[agent]'")

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

@pytest.fixture
def live_dcs_run_context(dcs_connection):
    yield RunContext(dcs_connection, model=TestModel(), usage=Usage())
