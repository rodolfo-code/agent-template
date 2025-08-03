"""
{{ cookiecutter.agent_name }} agent builder.
"""

import logging
from langgraph.graph import StateGraph
from app.domain.state.{{cookiecutter.agent_name}}_state import {{cookiecutter.agent_name}}State

from langgraph.graph import StateGraph, END, START

logger = logging.getLogger(__name__)


class {{cookiecutter.agent_builder_class_name}}:
    """Builder for {{ cookiecutter.agent_name }} using LangGraph."""
    
    def __init__(self):
        """Initialize the agent builder."""
        self.workflow = StateGraph({{cookiecutter.agent_name}}State)
        self._build_graph()
        self._build_agent = self._compile_agent()
    
    def _build_graph(self):
        self.workflow.add_node("{{cookiecutter.first_node_name}}.upper()", {{cookiecutter.first_node_name}})

        self.set_entry_point("{{cookiecutter.first_node_name}}.upper()")

        self.workflow.add_edge(START, "{{cookiecutter.first_node_name}}.upper()")

        self.workflow.add_edge("{{cookiecutter.first_node_name}}.upper()", END)

    def _build_graph(self):
        """Build the workflow graph."""
        pass
    
    def _compile_agent(self):
        return self.workflow.compile()

    def build_agent(self):
        print(self._build_agent.get_graph().draw_mermaid())
        return self._build_agent