"""
{{ cookiecutter.first_node_name }} node for {{ cookiecutter.agent_name }}.
"""

from typing import Dict, Any
from app.domain.state.{{cookiecutter.agent_name}}_state import {{cookiecutter.agent_name}}State


async def {{cookiecutter.first_node_name}}(state: {{cookiecutter.agent_name}}State) -> Dict[str, Any]:
    """{{ cookiecutter.first_node_name }} node."""
    pass 