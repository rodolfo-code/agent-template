"""
{{ cookiecutter.agent_name }} agent builder.
"""

import structlog
from langgraph.graph import StateGraph
from app.domain.state.agent_state import AgentState

logger = structlog.get_logger()


class AgentBuilder:
    """Builder for {{ cookiecutter.agent_name }} using LangGraph."""
    
    def __init__(self):
        """Initialize the agent builder."""
        self.workflow = StateGraph(AgentState)
        self._build_graph()
        self._build_agent = self._compile_agent()
    
    def build(self):
        """Build the agent workflow graph."""
        pass
    
    def _build_graph(self):
        """Build the workflow graph."""
        pass
    
    def _compile_agent(self):
        return self.workflow.compile()

    def build_agent(self):
        print(self._build_agent.get_graph().draw_mermaid())
        return self._build_agent