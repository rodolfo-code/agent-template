"""
{{ cookiecutter.agent_name }} service implementation.
"""

import time
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

import structlog

from app.application.agent.{{cookiecutter.agent_name}}.agent_builder.{{cookiecutter.agent_name}}_agent_builder import AgentBuilder
from app.domain.entities.{{cookiecutter.agent_name}}_output import AgentOutput, ProcessingStatus
from app.domain.state.{{cookiecutter.agent_name}}_state import create_initial_state
from app.infrastructure.config.config import get_agent_config

logger = structlog.get_logger()


class AgentService:
    """Service for {{ cookiecutter.agent_name }} processing."""
    
    def __init__(self):
        """Initialize the agent service."""
        self.agent_builder = AgentBuilder()
        self.config = get_agent_config()
        
        logger.info(
            "{{ cookiecutter.agent_name }} service initialized",
            config=self.config
        )
    
    async def process(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process content using the agent.
        
        Args:
            content: Content to process
            metadata: Optional metadata
            options: Optional processing options
            
        Returns:
            Processing result
        """
        processing_id = uuid4()
        start_time = time.time()
        
        # Initialize metadata and options
        metadata = metadata or {}
        options = options or {}
        
        logger.info(
            "Starting {{ cookiecutter.agent_name }} processing",
            processing_id=str(processing_id),
            content_length=len(content),
            metadata=metadata,
            options=options
        )
        
        try:
            # Create initial state
            reflection_enabled = options.get(
                "enable_reflection", 
                self.config["enable_reflection"]
            )
            
            initial_state = create_initial_state(
                content=content,
                metadata=metadata,
                processing_id=processing_id,
                reflection_enabled=reflection_enabled
            )
            
            # Build and run the agent
            agent = self.agent_builder.build()
            
            # Execute the agent workflow
            final_state = await agent.ainvoke(initial_state)
            
            execution_time = time.time() - start_time
            
            # Create output
            output = AgentOutput(
                id=processing_id,
                status=ProcessingStatus.COMPLETED,
                result=final_state.get("result"),
                confidence_score=final_state.get("confidence_score"),
                metadata={
                    "steps_completed": final_state.get("steps_completed", []),
                    "reflection_enabled": reflection_enabled,
                    "reflection_notes": final_state.get("reflection_notes"),
                },
                execution_time=execution_time,
                tokens_used=final_state.get("tokens_used", 0),
                created_at=final_state["started_at"],
                completed_at=datetime.utcnow()
            )
            
            logger.info(
                "{{ cookiecutter.agent_name }} processing completed",
                processing_id=str(processing_id),
                execution_time=execution_time,
                tokens_used=output.tokens_used,
                status=output.status
            )
            
            return output.dict()
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            logger.error(
                "{{ cookiecutter.agent_name }} processing failed",
                processing_id=str(processing_id),
                error=str(e),
                execution_time=execution_time,
                exc_info=True
            )
            
            # Create error output
            error_output = AgentOutput(
                id=processing_id,
                status=ProcessingStatus.FAILED,
                result=None,
                error_message=str(e),
                execution_time=execution_time,
                created_at=datetime.utcnow()
            )
            
            return error_output.dict()
    
    async def process_with_reflection(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process content with reflection enabled.
        
        Args:
            content: Content to process
            metadata: Optional metadata
            options: Optional processing options
            
        Returns:
            Processing result with reflection
        """
        # Ensure reflection is enabled
        options = options or {}
        options["enable_reflection"] = True
        
        return await self.process(content, metadata, options)
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the service.
        
        Returns:
            Health check result
        """
        try:
            # Simple test to ensure the agent can be built
            agent = self.agent_builder.build()
            
            return {
                "status": "healthy",
                "service": "{{ cookiecutter.agent_name }}_service",
                "agent_available": agent is not None,
                "config": self.config
            }
        except Exception as e:
            logger.error(
                "{{ cookiecutter.agent_name }} service health check failed",
                error=str(e),
                exc_info=True
            )
            
            return {
                "status": "unhealthy",
                "service": "{{ cookiecutter.agent_name }}_service",
                "error": str(e)
            } 