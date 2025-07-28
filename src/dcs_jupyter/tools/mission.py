"""DCS mission information tools."""

import textwrap

try:
    from pydantic_ai import RunContext
except ImportError:
    raise ImportError("PydanticAI is required for agent functionality. Install with: pip install 'dcs-jupyter[agent]'")

from dcs_jupyter.connection import DCSConnection, LuaExecutionError
from dcs_jupyter.tools.base import DCSToolResult


async def get_mission_info(ctx: RunContext[DCSConnection]) -> DCSToolResult:
    """Get current mission information from DCS World.
    
    Args:
        ctx: Runtime context containing DCS connection
        
    Returns:
        DCSToolResult with success flag and JSON data containing mission details
        including theatre, date, weather, coalitions, and other mission properties
    """
    
    lua_code = textwrap.dedent("""
        local mission_info = {
            theatre = env.mission.theatre,
            date = env.mission.date,
            start_time = env.mission.start_time,
            weather = env.mission.weather,
            coalitions = env.mission.coalitions,
            version = env.mission.version,
            descriptionText = env.mission.descriptionText,
            goals = env.mission.goals,
            map = env.mission.map
        }
        
        return net.lua2json(mission_info)
    """).strip()
    
    try:
        result = ctx.deps.execute(lua_code)
        return DCSToolResult(success=True, data=result)
    except LuaExecutionError as e:
        return DCSToolResult(success=False, data=str(e))