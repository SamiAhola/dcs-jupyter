"""DCS fog/weather tools."""

from dcs_jupyter.connection import DCSConnection
from dcs_jupyter.tools.base import DCSToolResult, handle_dcs_errors


def create_tool_set_fog_thickness(dcs: DCSConnection):
    def set_fog_thickness(thickness: float) -> DCSToolResult:
        """Set fog thickness in meters at sea level.
        
        Args:
            thickness: Fog thickness in meters (100-5000, 0 removes fog)
            
        Returns:
            DCSToolResult with success flag and confirmation data
        """
        lua_code = f"world.weather.setFogThickness({thickness})"
        return handle_dcs_errors(lambda: dcs.execute(lua_code))
    
    return set_fog_thickness


def create_tool_get_fog_thickness(dcs: DCSConnection):
    def get_fog_thickness() -> DCSToolResult:
        """Get current fog thickness in meters.
        
        Returns:
            DCSToolResult with success flag and current fog thickness data
        """
        lua_code = "return net.lua2json({fog_thickness = world.weather.getFogThickness()})"
        return handle_dcs_errors(lambda: dcs.execute(lua_code))
    
    return get_fog_thickness


def create_tool_set_fog_visibility_distance(dcs: DCSConnection):
    def set_fog_visibility_distance(distance: float) -> DCSToolResult:
        """Set fog visibility distance in meters.
        
        Args:
            distance: Visibility distance in meters
            
        Returns:
            DCSToolResult with success flag and confirmation data
        """
        lua_code = f"world.weather.setFogVisibilityDistance({distance})"
        return handle_dcs_errors(lambda: dcs.execute(lua_code))
    
    return set_fog_visibility_distance


def create_tool_get_fog_visibility_distance(dcs: DCSConnection):
    def get_fog_visibility_distance() -> DCSToolResult:
        """Get current fog visibility distance in meters.
        
        Returns:
            DCSToolResult with success flag and current fog visibility distance data
        """
        lua_code = "return net.lua2json({fog_visibility_distance = world.weather.getFogVisibilityDistance()})"
        return handle_dcs_errors(lambda: dcs.execute(lua_code))
    
    return get_fog_visibility_distance