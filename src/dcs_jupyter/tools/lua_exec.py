"""DCS Lua execution tool for arbitrary code execution."""

try:
    from pydantic_ai import RunContext
except ImportError:
    raise ImportError("PydanticAI is required for agent functionality. Install with: pip install 'dcs-jupyter[agent]'")

from dcs_jupyter.connection import DCSConnection, LuaExecutionError
from dcs_jupyter.tools.base import DCSToolResult


async def execute_lua(
    ctx: RunContext[DCSConnection],
    lua_code: str,
) -> DCSToolResult:
    """Execute arbitrary Lua code in the DCS scripting environment.

    Args:
        ctx: Runtime context containing DCS connection
        lua_code: Raw Lua code to execute in DCS

    Returns:
        JSON string containing the result of the Lua execution, or
        LuaExecutionError if execution fails in DCS

    Note:
        This tool allows direct access to the DCS scripting environment.
        Use net.lua2json() to return structured data as JSON.
        
    Examples:
        - Get current mission time: "return net.lua2json({time = timer.getTime()})"
        - List all units: "return net.lua2json({units = world.getUnits()})"
        - Get weather: "return net.lua2json({weather = world.weather})"
    """
    try:
        result = ctx.deps.execute(lua_code)
        return DCSToolResult(success=True, data=result)
    except LuaExecutionError as e:
        return DCSToolResult(success=False, data=str(e))
