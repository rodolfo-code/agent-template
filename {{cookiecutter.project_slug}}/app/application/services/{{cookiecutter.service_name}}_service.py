"""
{{ cookiecutter.service_name }} service implementation.
"""

from typing import Any, Dict, Optional

import logging

from app.application.agent.{{cookiecutter.agent_name}}.agent_builder.{{cookiecutter.agent_builder_name}} import {{cookiecutter.agent_builder_class_name}}
from app.domain.entities.{{cookiecutter.agent_name}}_output import AgentOutput, ProcessingStatus

logger = logging.getLogger(__name__)


class {{cookiecutter.service_class_name}}:
    """Service for {{ cookiecutter.service_name }} processing."""
    
    def __init__(self):
        """Initialize the agent service."""
        self.agent_builder = {{cookiecutter.agent_builder_class_name}}()
        self.agent = self.agent_builder.build_agent()

    def process_input(self, input_data: Any) -> Dict[str, Any]:
        try:

            # TODO: Criar o estado inicial
            # Exemplo:
            # initial_state: AgentState = {
            #     "input_data": input_data,
            #     "output_data": "",
            #     "status": ProcessingStatus.PENDING,
            # }

            # TODO: Processar o input
            # Exemplo:
            # result = self.agent.invoke(initial_state)

            logger.info(
                "Successfully processed data"
            )

            # return result

        except Exception as e:
            logger.error(
                "Error processing data",
                error=str(e),
            )
            raise