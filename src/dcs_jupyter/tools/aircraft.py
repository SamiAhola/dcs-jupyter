"""DCS aircraft tools."""

import textwrap
from string import Template

try:
    from pydantic_ai import RunContext
except ImportError:
    raise ImportError("PydanticAI is required for agent functionality. Install with: pip install 'dcs-jupyter[agent]'")

from dcs_jupyter.connection import DCSConnection, LuaExecutionError
from dcs_jupyter.tools.aircraft_types import AircraftType


async def spawn_aircraft(
    ctx: RunContext[DCSConnection],
    aircraft_type: AircraftType,
    x_coord: float,
    y_coord: float,
    altitude: float = 2000,
    group_id: int | None = None,
    unit_id: int | None = None,
    pilot_skill_level: str = 'High',
) -> str | LuaExecutionError:
    """Spawn an aircraft at the specified coordinates.

    Args:
        ctx: Runtime context containing DCS connection
        aircraft_type: DCS aircraft type from AircraftType enum
        x_coord: X coordinate in DCS world (East-West position)
        y_coord: Y coordinate in DCS world (North-South position, this is Z in DCS internal system)
        altitude: Altitude in meters above sea level (default: 2000m)
        group_id: Unique identifier for the aircraft group (optional, DCS auto-generates if None)
        unit_id: Unique identifier for the unit (optional, DCS auto-generates if None)
        pilot_skill_level: AI pilot skill ("Rookie", "Trained", "Veteran", "Ace", "High")

    Returns:
        JSON string containing spawned aircraft details including position and IDs

    Raises:
        LuaExecutionError: If spawn fails in DCS

    Note:
        DCS will auto-generate unique IDs if group_id or unit_id are None or conflict
        with existing groups/units. Groups/units with duplicate names will be destroyed.
    """

    lua_template = Template(
        textwrap.dedent("""
        -- Template variables from Python
        local aircraftType = "$aircraft_type"
        local xCoord = $x_coord
        local yCoord = $y_coord
        local altitude = $altitude
        local groupId = $group_id
        local unitId = $unit_id
        local skillLevel = "$pilot_skill_level"
        local routeAltitude = altitude

        local groupName = aircraftType .. "_Group"
        local unitName = aircraftType .. "_1"

        local groupData = {
            ["name"] = groupName,
            ["units"] = {
                [1] = {
                    ["name"] = unitName,
                    ["type"] = aircraftType,
                    ["x"] = xCoord,
                    ["y"] = yCoord,
                    ["alt"] = altitude,
                    ["skill"] = skillLevel
                }
            },
            ["route"] = {
                ["points"] = {
                    [1] = {
                        ["x"] = xCoord,
                        ["y"] = yCoord,
                        ["alt"] = routeAltitude,
                        ["type"] = "Turning Point"
                    }
                }
            }
        }

        -- Only add IDs if provided
        if groupId then
            groupData["groupId"] = groupId
        end
        if unitId then
            groupData["units"][1]["unitId"] = unitId
        end

        local newGroup = coalition.addGroup(coalition.side.BLUE, Group.Category.AIRPLANE, groupData)
        local actualGroupId = newGroup:getID()
        local actualUnitId = newGroup:getUnits()[1]:getID()

        return net.lua2json({
            groupId = actualGroupId,
            unitId = actualUnitId,
            groupName = groupName,
            unitName = unitName,
            aircraftType = aircraftType,
            position = {
                x = xCoord,
                y = yCoord,
                alt = altitude
            }
        })
    """).strip()
    )

    lua_code = lua_template.substitute(
        aircraft_type=aircraft_type,
        x_coord=x_coord,
        y_coord=y_coord,
        altitude=altitude,
        group_id=group_id if group_id is not None else 'nil',
        unit_id=unit_id if unit_id is not None else 'nil',
        pilot_skill_level=pilot_skill_level,
    )

    try:
        return ctx.deps.execute(lua_code)
    except LuaExecutionError as e:
        return e
