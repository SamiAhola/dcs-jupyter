"""Simple DCS agent with PydanticAI."""

import argparse
import os
import textwrap
from string import Template

try:
    from pydantic_ai import Agent, RunContext
    from pydantic_ai.exceptions import AgentRunError
except ImportError:
    raise ImportError("PydanticAI is required for agent functionality. Install with: pip install 'dcs-jupyter[agent]'")
try:
    import logfire

    logfire.configure(send_to_logfire=False)
except ImportError:
    pass

from dcs_jupyter.connection import DCSConnection


# Model presets for common AI providers
MODEL_PRESETS = {
    # Anthropic Claude models
    'claude': 'claude-sonnet-4-20250514',
    'claude-3-5-sonnet': 'claude-3-5-sonnet-20241022',
    'claude-3-5-haiku': 'claude-3-5-haiku-20241022',
    # OpenAI models
    'gpt-4': 'gpt-4',
    'gpt-4-turbo': 'gpt-4-turbo',
    'gpt-4o': 'gpt-4o',
    'gpt-4o-mini': 'gpt-4o-mini',
    # Default
    'default': 'claude-sonnet-4-20250514',
}


def spawn_aircraft(
    ctx: RunContext[DCSConnection], 
    aircraft_type: str, 
    airbase_name: str,
    group_id: int | None = None,
    unit_id: int | None = None,
    altitude_offset_meters: int = 1000,
    pilot_skill_level: str = 'High',
) -> str:
    """Spawn an aircraft at the specified airbase location.

    Args:
        ctx: Runtime context containing DCS connection
        aircraft_type: DCS aircraft type (e.g., "F-16C_50", "A-10C_2")
        airbase_name: Name of the airbase where aircraft will spawn
        group_id: Unique identifier for the aircraft group (optional, DCS auto-generates if None)
        unit_id: Unique identifier for the unit (optional, DCS auto-generates if None)
        altitude_offset_meters: Altitude offset above airbase (default: 500m)
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
    
    return ctx.deps.execute(lua_code)


def create_dcs_agent(model: str | None = None) -> Agent[DCSConnection]:
    """Create PydanticAI agent with DCS tools.

    Args:
        model: Model name or preset. If None, uses environment variable DCS_AGENT_MODEL
               or defaults to 'claude'. Supports presets like 'claude', 'gpt-4', etc.
    """
    if model is None:
        model = os.environ.get('DCS_AGENT_MODEL', 'default')

    # Resolve model preset if applicable
    resolved_model = MODEL_PRESETS.get(model, model)

    agent = Agent(
        resolved_model,
        system_prompt='You are a DCS World mission controller. Use available tools to execute user commands.',
        tools=[spawn_aircraft],
        deps_type=DCSConnection,
        instrument=True,
    )

    return agent


def main():
    """Main entry point for the DCS agent CLI."""
    parser = argparse.ArgumentParser(
        description='DCS World AI Agent - Natural language mission control',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            f"""
            Available model presets:
            {chr(10).join(f'  {preset}: {model}' for preset, model in MODEL_PRESETS.items())}

            Environment variables:
              DCS_AGENT_MODEL: Set default model (overridden by --model)
              ANTHROPIC_API_KEY: For Claude models
              OPENAI_API_KEY: For OpenAI models

            Examples:
              python -m dcs_jupyter.agent --model claude
              python -m dcs_jupyter.agent --model gpt-4o
              DCS_AGENT_MODEL=gpt-4 python -m dcs_jupyter.agent
            """
        ),
    )

    parser.add_argument('--model', '-m', help='AI model to use (preset name or full model identifier)', default=None)

    parser.add_argument('--list-models', action='store_true', help='List available model presets and exit')

    args = parser.parse_args()

    if args.list_models:
        print('Available model presets:')
        for preset, model in MODEL_PRESETS.items():
            print(f'  {preset:<15} -> {model}')
        return

    try:
        dcs_connection = DCSConnection()
        agent = create_dcs_agent(args.model)
        agent.to_cli_sync(deps=dcs_connection)
    except KeyboardInterrupt:
        print('\nAgent terminated by user')
    except Exception as e:
        print(f'Error: {e}')
        return 1


if __name__ == '__main__':
    main()
