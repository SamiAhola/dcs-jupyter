"""Simple DCS World MCP Server - Execute Lua code in DCS World."""

import sys

try:
    from fastmcp import FastMCP
except ImportError:
    print("Error: FastMCP not installed. Run: pip install 'dcs-jupyter[agent]'", file=sys.stderr)
    sys.exit(1)

from dcs_jupyter.connection import DCSConnection
from dcs_jupyter.tools import create_tool_execute_lua


def main():
    dcs = DCSConnection()
    mcp: FastMCP = FastMCP(name='dcs-world-mcp', tools=[create_tool_execute_lua(dcs)])

    """Run the MCP server."""
    print('Starting DCS World MCP Server...')
    mcp.run()


if __name__ == '__main__':
    main()
