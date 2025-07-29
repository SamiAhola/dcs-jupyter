"""Simple DCS World MCP Server - Execute Lua code in DCS World."""

import sys

try:
    from fastmcp import FastMCP
except ImportError:
    print("Error: FastMCP not installed. Run: pip install 'dcs-jupyter[agent]'", file=sys.stderr)
    sys.exit(1)

from dcs_jupyter.connection import DCSConnection
from dcs_jupyter.tools import (
    create_tool_execute_lua,
    create_tool_get_airbases,
    create_tool_spawn_aircraft,
    create_tool_get_mission_info,
)


def main() -> None:
    dcs = DCSConnection()
    mcp: FastMCP = FastMCP(
        name='dcs-world-mcp',
        tools=[
            create_tool_execute_lua(dcs),
            create_tool_get_airbases(dcs),
            create_tool_spawn_aircraft(dcs),
            create_tool_get_mission_info(dcs),
        ],
    )

    """Run the MCP server."""
    print('Starting DCS World MCP Server...')
    mcp.run()


if __name__ == '__main__':
    main()
