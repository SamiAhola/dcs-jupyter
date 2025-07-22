"""Simple DCS agent with PydanticAI."""

import argparse
import os
import textwrap

try:
    from pydantic_ai import Agent
except ImportError:
    raise ImportError("PydanticAI is required for agent functionality. Install with: pip install 'dcs-jupyter[agent]'")
try:
    import logfire
    logfire.configure(send_to_logfire=False)
except ImportError:
    pass

from dcs_jupyter.connection import DCSConnection
from dcs_jupyter.tools import get_airbases, spawn_aircraft


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
        tools=[get_airbases, spawn_aircraft],
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
