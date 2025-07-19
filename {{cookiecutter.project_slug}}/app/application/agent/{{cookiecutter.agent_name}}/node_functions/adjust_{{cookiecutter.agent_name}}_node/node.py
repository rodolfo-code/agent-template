"""
Adjustment node for {{ cookiecutter.agent_name }}.
"""

import time
from datetime import datetime
from typing import Dict, Any

import structlog

from app.domain.state.{{cookiecutter.agent_name}}_state import AgentState, update_state_step

logger = structlog.get_logger()


async def adjust_processing_node(state: AgentState) -> Dict[str, Any]:
    """Adjustment node for {{ cookiecutter.agent_name }}.
    
    This node makes adjustments based on reflection feedback.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state dictionary
    """
    logger.info("Executing adjustment node")
    
    start_time = time.time()
    
    try:
        # Update state
        state = update_state_step(state, "adjust_processing")
        
        # Get reflection notes and improvements
        reflection_notes = state.get("reflection_notes", "")
        improvements = state.get("improvement_suggestions", [])
        
        # Simple adjustment logic - reset for retry
        execution_time = time.time() - start_time
        
        logger.info(
            "Adjustment completed",
            execution_time=execution_time,
            improvements_count=len(improvements)
        )
        
        # Prepare for retry with adjustments
        return {
            "current_step": "adjust_processing",
            "last_updated_at": datetime.utcnow(),
            "execution_metadata": {
                **state.get("execution_metadata", {}),
                "adjustment": {
                    "execution_time": execution_time,
                    "improvements_applied": improvements,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        }
        
    except Exception as e:
        execution_time = time.time() - start_time
        
        logger.error(
            "Adjustment node failed",
            error=str(e),
            execution_time=execution_time,
            exc_info=True
        )
        
        return {
            "error_messages": [f"Adjustment failed: {str(e)}"],
            "current_step": "adjust_processing",
            "last_updated_at": datetime.utcnow()
        } 