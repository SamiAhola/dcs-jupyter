"""Base types and protocols for DCS tools."""

from pydantic import BaseModel


class DCSToolResult(BaseModel):
    """Structured result for all DCS tool operations."""

    success: bool
    data: str
