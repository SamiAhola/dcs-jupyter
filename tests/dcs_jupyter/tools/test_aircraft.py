"""Unit tests for DCS aircraft tools with direct function calls."""
import pytest
from dcs_jupyter.tools.aircraft import spawn_aircraft
from dcs_jupyter.connection import LuaExecutionError


@pytest.mark.asyncio
async def test_spawn_aircraft_direct(live_dcs_run_context):
    """Test spawn_aircraft tool function directly using coordinates."""
    # Call the tool function directly
    result = await spawn_aircraft(
        ctx=live_dcs_run_context,
        aircraft_type='F/A-18C',
        x_coord=10.0,
        y_coord=10.0,
        altitude=2000.0
    )
    
    match result:
        case str() as response:
            print(f"Tool Response: {response}")
        case LuaExecutionError() as error:
            print(f"Tool Error: {error}")
            pytest.fail(f"Spawning aircraft failed: {error}")
