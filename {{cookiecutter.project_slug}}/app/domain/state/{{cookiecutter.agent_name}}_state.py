"""
{{ cookiecutter.agent_name }} state.
"""
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from typing_extensions import TypedDict


class {{cookiecutter.agent_name}}State(TypedDict):
    """State do agente."""
    pass 