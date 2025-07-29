"""Simple DCS World MCP Server - Execute Lua code in DCS World."""

import sys

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: MCP not installed. Run: pip install 'dcs-jupyter[mcp]'", file=sys.stderr)
    sys.exit(1)

from dcs_jupyter.connection import DCSConnection, LuaExecutionError

# Create MCP server and DCS connection
mcp = FastMCP(name="dcs-world-mcp")
dcs: DCSConnection | None = None


@mcp.tool()
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
    global dcs
    
    # Create connection if needed
    if dcs is None:
        dcs = DCSConnection()
    
    try:
        return dcs.execute(lua_code)
    except LuaExecutionError as e:
        raise Exception(f"DCS Lua error: {str(e)}")
    except Exception as e:
        raise Exception(f"Connection error: {str(e)}")


def main():
    """Run the MCP server."""
    print("Starting DCS World MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main()
