"""
Tests for DCS connection functionality.
"""


def test_dcs_connection(dcs_connection):
    """Test that the DCS connection fixture works properly."""
    # Simply executing a basic Lua command to verify connection
    result = dcs_connection.execute("return 'connected'")
    assert result == 'connected'
