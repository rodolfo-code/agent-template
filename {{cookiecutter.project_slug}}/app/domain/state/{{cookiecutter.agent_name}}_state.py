"""
{{ cookiecutter.agent_name }} state management for LangGraph.
"""

import operator
from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional
from uuid import UUID

from typing_extensions import TypedDict


class AgentState(TypedDict):
    """State management for {{ cookiecutter.agent_name }} workflow."""
    
    # Input data
    input_content: str
    input_metadata: Dict[str, Any]
    processing_id: UUID
    
    # Processing state
    current_step: str
    steps_completed: Annotated[List[str], operator.add]
    
    # Agent outputs
    result: Optional[str]
    intermediate_results: Annotated[List[str], operator.add]
    
    # Metadata and tracking
    execution_metadata: Dict[str, Any]
    error_messages: Annotated[List[str], operator.add]
    
    # Reflection and improvement
    reflection_enabled: bool
    reflection_notes: Optional[str]
    improvement_suggestions: Annotated[List[str], operator.add]
    
    # Performance tracking
    tokens_used: int
    execution_time: float
    confidence_score: Optional[float]
    
    # Timestamps
    started_at: datetime
    last_updated_at: datetime


class NodeInput(TypedDict):
    """Input structure for agent nodes."""
    
    content: str
    metadata: Dict[str, Any]
    options: Dict[str, Any]


class NodeOutput(TypedDict):
    """Output structure for agent nodes."""
    
    result: str
    metadata: Dict[str, Any]
    confidence_score: Optional[float]
    execution_time: float
    tokens_used: int


class ReflectionState(TypedDict):
    """State for reflection operations."""
    
    original_result: str
    reflection_prompt: str
    reflection_result: Optional[str]
    improvement_areas: List[str]
    confidence_assessment: Optional[float]


def create_initial_state(
    content: str,
    metadata: Dict[str, Any],
    processing_id: UUID,
    reflection_enabled: bool = True
) -> AgentState:
    """Create initial agent state.
    
    Args:
        content: Input content to process
        metadata: Input metadata
        processing_id: Unique processing identifier
        reflection_enabled: Whether reflection is enabled
        
    Returns:
        Initial agent state
    """
    now = datetime.utcnow()
    
    return AgentState(
        # Input data
        input_content=content,
        input_metadata=metadata,
        processing_id=processing_id,
        
        # Processing state
        current_step="start",
        steps_completed=[],
        
        # Agent outputs
        result=None,
        intermediate_results=[],
        
        # Metadata and tracking
        execution_metadata={},
        error_messages=[],
        
        # Reflection and improvement
        reflection_enabled=reflection_enabled,
        reflection_notes=None,
        improvement_suggestions=[],
        
        # Performance tracking
        tokens_used=0,
        execution_time=0.0,
        confidence_score=None,
        
        # Timestamps
        started_at=now,
        last_updated_at=now
    )


def update_state_step(state: AgentState, step_name: str) -> AgentState:
    """Update state when moving to a new step.
    
    Args:
        state: Current agent state
        step_name: Name of the new step
        
    Returns:
        Updated agent state
    """
    state["current_step"] = step_name
    state["steps_completed"].append(step_name)
    state["last_updated_at"] = datetime.utcnow()
    return state


def add_error_to_state(state: AgentState, error_message: str) -> AgentState:
    """Add error message to state.
    
    Args:
        state: Current agent state
        error_message: Error message to add
        
    Returns:
        Updated agent state
    """
    state["error_messages"].append(error_message)
    state["last_updated_at"] = datetime.utcnow()
    return state 