"""DCS airbase tools."""

import textwrap

try:
    from pydantic_ai import RunContext
except ImportError:
    raise ImportError("PydanticAI is required for agent functionality. Install with: pip install 'dcs-jupyter[agent]'")

from dcs_jupyter.connection import DCSConnection, LuaExecutionError
from dcs_jupyter.tools.base import DCSToolResult


async def get_airbases(
    ctx: RunContext[DCSConnection],
) -> DCSToolResult:
    """Get all available airbases with detailed information.

    Args:
        ctx: Runtime context containing DCS connection

    Returns:
        DCSToolResult with success flag and JSON data containing list of airbases
    """

    lua_code = textwrap.dedent("""
        local base = world.getAirbases()
        local airbases = {}
        
        for i = 1, #base do
            local info = {}
            info.callsign = Airbase.getCallsign(base[i])
            info.id = Airbase.getID(base[i])
            info.cat = Airbase.getDesc(base[i]).category
            info.point = Airbase.getPoint(base[i])
            
            if Airbase.getUnit(base[i]) then
                info.unitId = Airbase.getUnit(base[i]):getID()
            end
            
            -- Determine coalition
            local coalitionId = base[i]:getCoalition()
            if coalitionId == 0 then
                info.coalition = "neutral"
            elseif coalitionId == 1 then
                info.coalition = "red"
            elseif coalitionId == 2 then
                info.coalition = "blue"
            else
                info.coalition = "unknown"
            end
            
            table.insert(airbases, info)
        end
        
        return net.lua2json({
            airbases = airbases,
            count = #airbases
        })
        """).strip()

    try:
        result = ctx.deps.execute(lua_code)
        return DCSToolResult(success=True, data=result)
    except LuaExecutionError as e:
        return DCSToolResult(success=False, data=str(e))
