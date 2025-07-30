"""Base types and protocols for DCS tools."""

from typing import Callable

from pydantic import BaseModel

from dcs_jupyter.connection import DCSConnection, LuaExecutionError


class DCSToolResult(BaseModel):
    """Structured result for all DCS tool operations."""

    success: bool
    data: str


def handle_dcs_errors(operation: Callable[[], str]) -> DCSToolResult:
    """Execute an operation with standardized DCS error handling.

    Args:
        operation: Callable that performs the actual operation

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
