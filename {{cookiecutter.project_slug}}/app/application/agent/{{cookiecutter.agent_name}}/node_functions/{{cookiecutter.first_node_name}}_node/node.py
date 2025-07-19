"""
{{ cookiecutter.first_node_name }} node for {{ cookiecutter.agent_name }}.
"""

from typing import Dict, Any
from app.domain.state.agent_state import AgentState


async def first_node(state: AgentState) -> Dict[str, Any]:
    """{{ cookiecutter.first_node_name }} node."""
    pass 