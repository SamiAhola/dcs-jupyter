"""DCS aircraft tools."""

import textwrap
from string import Template

try:
    from pydantic_ai import RunContext
    from pydantic_ai.exceptions import AgentRunError
except ImportError:
    raise ImportError("PydanticAI is required for agent functionality. Install with: pip install 'dcs-jupyter[agent]'")

from dcs_jupyter.connection import DCSConnection, LuaExecutionError
from dcs_jupyter.tools.aircraft_types import AircraftType


async def spawn_aircraft(
    ctx: RunContext[DCSConnection],
    aircraft_type: AircraftType,
    airbase_name: str,
    group_id: int | None = None,
    unit_id: int | None = None,
    altitude_offset_meters: int = 1000,
    pilot_skill_level: str = 'High',
) -> str:
    """Spawn an aircraft at the specified airbase location.

    Args:
        ctx: Runtime context containing DCS connection
        aircraft_type: DCS aircraft type from AircraftType enum
        airbase_name: Name of the airbase where aircraft will spawn
        group_id: Unique identifier for the aircraft group (optional, DCS auto-generates if None)
        unit_id: Unique identifier for the unit (optional, DCS auto-generates if None)
        altitude_offset_meters: Altitude offset above airbase (default: 1000m)
        pilot_skill_level: AI pilot skill ("Rookie", "Trained", "Veteran", "Ace", "High")

    Returns:
        JSON string containing spawned aircraft details including position and IDs

    Raises:
        LuaExecutionError: If airbase not found or spawn fails in DCS

    Note:
        DCS will auto-generate unique IDs if group_id or unit_id are None or conflict
        with existing groups/units. Groups/units with duplicate names will be destroyed.
    """

    lua_template = Template(
        textwrap.dedent("""
        -- Template variables from Python
        local airbaseName = "$airbase_name"
        local aircraftType = "$aircraft_type"
        local groupId = $group_id
        local unitId = $unit_id
        local altitudeOffset = $altitude_offset_meters
        local skillLevel = "$pilot_skill_level"
        local routeAltitude = 2000

        local airbase = Airbase.getByName(airbaseName)
        if not airbase then
            error("Airbase '" .. airbaseName .. "' not found")
        end

        local position = airbase:getPosition().p
        local groupName = aircraftType .. "_Group"
        local unitName = aircraftType .. "_1"

        local groupData = {
            ["name"] = groupName,
            ["units"] = {
                [1] = {
                    ["name"] = unitName,
                    ["type"] = aircraftType,
                    ["x"] = position.x,
                    ["y"] = position.z,
                    ["alt"] = position.y + altitudeOffset,
                    ["skill"] = skillLevel
                }
            },
            ["route"] = {
                ["points"] = {
                    [1] = {
                        ["x"] = position.x,
                        ["y"] = position.z,
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
            location = airbaseName,
            position = {
                x = position.x,
                y = position.z,
                alt = position.y + altitudeOffset
            }
        })
    """).strip()
    )

    lua_code = lua_template.substitute(
        airbase_name=airbase_name,
        aircraft_type=aircraft_type,
        group_id=group_id if group_id is not None else 'nil',
        unit_id=unit_id if unit_id is not None else 'nil',
        altitude_offset_meters=altitude_offset_meters,
        pilot_skill_level=pilot_skill_level,
    )

    try:
        return ctx.deps.execute(lua_code)
    except LuaExecutionError as e:
        raise AgentRunError("Error executing lua code.") from e