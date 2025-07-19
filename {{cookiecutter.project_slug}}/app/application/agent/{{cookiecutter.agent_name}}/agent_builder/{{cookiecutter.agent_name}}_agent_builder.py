"""
{{ cookiecutter.agent_name }} Agent Builder using LangGraph.
"""

import structlog
from langgraph.graph import StateGraph

from app.application.agent.{{cookiecutter.agent_name}}.agent_builder.decision_router import decision_router
from app.application.agent.{{cookiecutter.agent_name}}.node_functions.{{cookiecutter.agent_name}}_node import main_processing_node
from app.application.agent.{{cookiecutter.agent_name}}.node_functions.adjust_{{cookiecutter.agent_name}}_node import adjust_processing_node
from app.application.agent.{{cookiecutter.agent_name}}.node_functions.reflect_node import reflection_node
from app.domain.state.{{cookiecutter.agent_name}}_state import AgentState

logger = structlog.get_logger()


class AgentBuilder:
    """Builder for {{ cookiecutter.agent_name }} using LangGraph."""
    
    def __init__(self):
        """Initialize the agent builder."""
        logger.info("Initializing {{ cookiecutter.agent_name }} Agent Builder")
    
    def build(self) -> StateGraph:
        """Build the agent workflow graph.
        
        Returns:
            Compiled LangGraph workflow
        """
        logger.info("Building {{ cookiecutter.agent_name }} workflow")
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("main_processing", main_processing_node)
        workflow.add_node("reflection", reflection_node)
        workflow.add_node("adjust_processing", adjust_processing_node)
        
        # Define the entry point
        workflow.set_entry_point("main_processing")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "main_processing",
            decision_router,
            {
                "reflect": "reflection",
                "adjust": "adjust_processing",
                "end": "__end__"
            }
        )
        
        # Add edges from reflection
        workflow.add_conditional_edges(
            "reflection",
            decision_router,
            {
                "adjust": "adjust_processing",
                "end": "__end__"
            }
        )
        
        # Add edge from adjust back to main
        workflow.add_edge("adjust_processing", "main_processing")
        
        # Compile the graph
        compiled_workflow = workflow.compile()
        
        logger.info("{{ cookiecutter.agent_name }} workflow built successfully")
        
        return compiled_workflow
    
    def get_workflow_schema(self) -> dict:
        """Get the workflow schema for documentation.
        
        Returns:
            Workflow schema dictionary
        """
        return {
            "name": "{{ cookiecutter.agent_name }}_workflow",
            "description": "{{ cookiecutter.description }}",
            "nodes": [
                {
                    "name": "main_processing",
                    "description": "Main processing node for {{ cookiecutter.domain_name }} content",
                    "type": "processing"
                },
                {
                    "name": "reflection",
                    "description": "Reflection node for quality assessment",
                    "type": "reflection"
                },
                {
                    "name": "adjust_processing",
                    "description": "Adjustment node for improving results",
                    "type": "adjustment"
                }
            ],
            "edges": [
                {
                    "from": "main_processing",
                    "to": "reflection|adjust_processing|end",
                    "condition": "decision_router"
                },
                {
                    "from": "reflection",
                    "to": "adjust_processing|end",
                    "condition": "decision_router"
                },
                {
                    "from": "adjust_processing",
                    "to": "main_processing",
                    "condition": "direct"
                }
            ],
            "entry_point": "main_processing"
        } 