"""
{{ cookiecutter.agent_name }} service implementation.
"""

from typing import Any, Dict, Optional

import structlog

from app.application.agent.{{cookiecutter.agent_name}}.agent_builder.{{cookiecutter.agent_name}}_agent_builder import AgentBuilder
from app.domain.entities.{{cookiecutter.agent_name}}_output import AgentOutput, ProcessingStatus
from app.domain.state.{{cookiecutter.agent_name}}_state import create_initial_state

logger = structlog.get_logger()


class AgentService:
    """Service for {{ cookiecutter.agent_name }} processing."""
    
    def __init__(self):
        """Initialize the agent service."""
        self.agent_builder = AgentBuilder()
        self.config = self.agent_builder.build_agent()
        
        logger.info(
            "{{ cookiecutter.agent_name }} service initialized",
            config=self.config
        )