"""Simple DCS World MCP Server - Execute Lua code in DCS World."""

import sys

try:
    from fastmcp import FastMCP
except ImportError:
    print("Error: FastMCP not installed. Run: pip install 'dcs-jupyter[agent]'", file=sys.stderr)
    sys.exit(1)

from dcs_jupyter.connection import DCSConnection, LuaExecutionError


def create_tool_execute_lua(dcs: DCSConnection):
    def execute_lua(lua_code: str) -> str:
        """Execute arbitrary Lua code in DCS World.
        
        Args:
            lua_code: Raw Lua code to execute in DCS World
            
        Returns:
            String result from DCS Lua execution
            
        Examples:
            - Get mission time: "return timer.getTime()"
            - Get units as JSON: "return net.lua2json({units = world.getUnits()})"
            - List airbases: "return net.lua2json({airbases = world.getAirbases()})"
        """
        
        try:
            return dcs.execute(lua_code)
        except LuaExecutionError as e:
            raise Exception(f"DCS Lua error: {str(e)}")
        except Exception as e:
            raise Exception(f"Connection error: {str(e)}")

    return execute_lua


def main():
    dcs = DCSConnection()
    mcp: FastMCP = FastMCP(name="dcs-world-mcp",
                           tools=[create_tool_execute_lua(dcs)])

    """Run the MCP server."""
    print("Starting DCS World MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main()
