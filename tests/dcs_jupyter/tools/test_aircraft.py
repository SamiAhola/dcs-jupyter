"""Unit tests for DCS aircraft tools with direct function calls."""
import pytest
from dcs_jupyter.tools.aircraft import create_tool_spawn_aircraft
from dcs_jupyter.connection import LuaExecutionError
from dcs_jupyter.tools.base import DCSToolResult


@pytest.mark.asyncio
async def test_spawn_aircraft_direct(dcs_connection):
    """Test spawn_aircraft tool function directly using coordinates."""
    # Create the tool function
    spawn_aircraft = create_tool_spawn_aircraft(dcs_connection)
    
    # Call the tool function directly
    result = spawn_aircraft(
        aircraft_type='F/A-18C',
        x_coord=10.0,
        y_coord=10.0,
        altitude=2000.0
    )
    
    match result:
        case DCSToolResult(success=True) as success_result:
            print(f"Tool Response: {success_result.data}")
        case DCSToolResult(success=False) as error_result:
            print(f"Tool Error: {error_result.data}")
            pytest.fail(f"Spawning aircraft failed: {error_result.data}")
        case _:
            pytest.fail(f"Unexpected result type: {type(result)}")
