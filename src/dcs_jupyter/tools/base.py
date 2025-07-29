"""Base types and protocols for DCS tools."""

from typing import Callable

from pydantic import BaseModel

from dcs_jupyter.connection import DCSConnection, LuaExecutionError


class DCSToolResult(BaseModel):
    """Structured result for all DCS tool operations."""

    success: bool
    data: str


def execute_dcs_tool(dcs: DCSConnection, operation: Callable[[], str]) -> DCSToolResult:
    """Execute a DCS tool operation with standardized error handling.

    Args:
        dcs: DCS connection instance
        operation: Callable that performs the actual DCS operation

    Returns:
        Standardized DCSToolResult with success flag and result/error data
    """
    try:
        result = operation()
        return DCSToolResult(success=True, data=result)
    except LuaExecutionError as e:
        return DCSToolResult(success=False, data=str(e))
    except Exception as e:
        return DCSToolResult(success=False, data=f'Connection error: {str(e)}')
