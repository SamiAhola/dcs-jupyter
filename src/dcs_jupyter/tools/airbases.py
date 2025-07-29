"""DCS airbase tools."""

import textwrap

from dcs_jupyter.connection import DCSConnection, LuaExecutionError
from dcs_jupyter.tools.base import DCSToolResult


def create_tool_get_airbases(dcs: DCSConnection):
    def get_airbases() -> DCSToolResult:
        """Get all available airbases with detailed information.

        Returns:
            DCSToolResult with success flag and JSON data containing list of airbases
        """

        lua_code = textwrap.dedent("""
            local base = world.getAirbases()
            local airbases = {}
            
            for i = 1, #base do
                local info = {}
                info.callsign = Airbase.getCallsign(base[i])
                info.id = Airbase.getID(base[i])
                info.cat = Airbase.getDesc(base[i]).category
                info.point = Airbase.getPoint(base[i])
                
                if Airbase.getUnit(base[i]) then
                    info.unitId = Airbase.getUnit(base[i]):getID()
                end
                
                -- Determine coalition
                local coalitionId = base[i]:getCoalition()
                if coalitionId == 0 then
                    info.coalition = "neutral"
                elseif coalitionId == 1 then
                    info.coalition = "red"
                elseif coalitionId == 2 then
                    info.coalition = "blue"
                else
                    info.coalition = "unknown"
                end
                
                table.insert(airbases, info)
            end
            
            return net.lua2json({
                airbases = airbases,
                count = #airbases
            })
            """).strip()

        try:
            result = dcs.execute(lua_code)
            return DCSToolResult(success=True, data=result)
        except LuaExecutionError as e:
            return DCSToolResult(success=False, data=str(e))
        except Exception as e:
            return DCSToolResult(success=False, data=f'Connection error: {str(e)}')

    return get_airbases
