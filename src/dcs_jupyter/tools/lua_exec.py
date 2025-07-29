"""DCS Lua execution tool for arbitrary code execution."""

from dcs_jupyter.connection import DCSConnection
from dcs_jupyter.tools.base import DCSToolResult, execute_dcs_tool


def create_tool_execute_lua(dcs: DCSConnection):
    def execute_lua(lua_code: str) -> DCSToolResult:
        """Execute arbitrary Lua code in the DCS scripting environment.

        Args:
            lua_code: Raw Lua code to execute in DCS

        Returns:
            DCSToolResult with success flag and data containing the result of the Lua execution

        Note:
            This tool allows direct access to the DCS scripting environment.
            Use net.lua2json() to return structured data as JSON.

        Examples:
            - Get current mission time: "return net.lua2json({time = timer.getTime()})"
            - List all units: "return net.lua2json({units = world.getUnits()})"
            - Get weather: "return net.lua2json({weather = world.weather})"
        """
        return execute_dcs_tool(dcs, lambda: dcs.execute(lua_code))

    return execute_lua
