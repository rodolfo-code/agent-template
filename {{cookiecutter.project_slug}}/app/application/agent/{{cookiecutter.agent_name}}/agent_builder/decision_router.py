"""
Decision router for {{ cookiecutter.agent_name }} workflow.
"""

import structlog
from typing import Literal

from app.domain.state.{{cookiecutter.agent_name}}_state import AgentState

logger = structlog.get_logger()


def decision_router(state: AgentState) -> Literal["reflect", "adjust", "end"]:
    """Route decisions in the {{ cookiecutter.agent_name }} workflow.
    
    This function determines the next step in the workflow based on the current state.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node to execute: "reflect", "adjust", or "end"
    """
    
    # Get current step and other relevant state information
    current_step = state.get("current_step", "")
    steps_completed = state.get("steps_completed", [])
    reflection_enabled = state.get("reflection_enabled", False)
    error_messages = state.get("error_messages", [])
    result = state.get("result")
    confidence_score = state.get("confidence_score")
    
    logger.debug(
        "Decision routing",
        current_step=current_step,
        steps_completed=steps_completed,
        reflection_enabled=reflection_enabled,
        has_errors=len(error_messages) > 0,
        has_result=result is not None,
        confidence_score=confidence_score
    )
    
    # If there are errors and we haven't tried adjusting yet, try adjustment
    if error_messages and "adjust_processing" not in steps_completed:
        logger.info("Routing to adjustment due to errors")
        return "adjust"
    
    # If coming from main processing and reflection is enabled
    if current_step == "main_processing":
        # If reflection is enabled and not done yet
        if reflection_enabled and "reflection" not in steps_completed:
            logger.info("Routing to reflection")
            return "reflect"
        
        # If we have a good result (high confidence), end
        if confidence_score is not None and confidence_score >= 0.8:
            logger.info("Routing to end due to high confidence")
            return "end"
        
        # If we've tried multiple times without improvement, end
        if len(steps_completed) >= 5:
            logger.info("Routing to end due to max attempts")
            return "end"
        
        # Otherwise end if we have a result
        if result is not None:
            logger.info("Routing to end with result")
            return "end"
    
    # If coming from reflection
    if current_step == "reflection":
        reflection_notes = state.get("reflection_notes")
        
        # If reflection suggests improvement and we haven't maxed out attempts
        if (reflection_notes and 
            "improvement" in reflection_notes.lower() and 
            len(steps_completed) < 4):
            logger.info("Routing to adjustment based on reflection")
            return "adjust"
        
        # Otherwise end
        logger.info("Routing to end from reflection")
        return "end"
    
    # If coming from adjustment, we might need another iteration
    if current_step == "adjust_processing":
        # If we've tried too many times, end
        if len(steps_completed) >= 5:
            logger.info("Routing to end due to max adjustment attempts")
            return "end"
        
        # If we have a good confidence score, end
        if confidence_score is not None and confidence_score >= 0.7:
            logger.info("Routing to end due to improved confidence")
            return "end"
        
        # Continue with main processing for another iteration
        logger.info("Continuing iteration after adjustment")
        return "end"  # This will go back to main_processing via the edge
    
    # Default: end the workflow
    logger.info("Default routing to end")
    return "end"


def should_continue_processing(state: AgentState) -> bool:
    """Check if processing should continue.
    
    Args:
        state: Current agent state
        
    Returns:
        True if processing should continue
    """
    steps_completed = state.get("steps_completed", [])
    error_messages = state.get("error_messages", [])
    result = state.get("result")
    confidence_score = state.get("confidence_score")
    
    # Stop if too many attempts
    if len(steps_completed) >= 5:
        return False
    
    # Stop if we have a good result
    if result and confidence_score and confidence_score >= 0.8:
        return False
    
    # Continue if we have errors to resolve
    if error_messages and len(steps_completed) < 3:
        return True
    
    # Continue if no result yet
    if not result:
        return True
    
    return False 