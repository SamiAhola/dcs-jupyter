"""Unit tests for DCS agent with live connection."""
import pytest
from dcs_jupyter.agent import create_dcs_agent
from dcs_jupyter.connection import LuaExecutionError


@pytest.mark.live_agent
def test_spawn_aircraft(dcs_connection):
    """Test agent spawn aircraft command using coordinates."""
    agent = create_dcs_agent()

    result = agent.run_sync(
        "Spawn an F-16A at coordinates 10.0, 10.0, altitude 2000.0", 
        deps=dcs_connection
    )
    
    match result.output:
        case str() as response:
            print(f"Agent Response: {response}")
        case LuaExecutionError() as error:
            print(f"Agent Error: {error}")
            pytest.fail(f"Spawning aircraft failed: {error}")
