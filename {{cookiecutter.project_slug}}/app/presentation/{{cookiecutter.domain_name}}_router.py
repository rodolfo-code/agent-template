"""
FastAPI router for {{ cookiecutter.domain_name }} processing.
"""

import structlog
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.application.services.{{cookiecutter.agent_name}}_service import AgentService
from app.domain.entities.{{cookiecutter.domain_name}} import DomainRequest

logger = structlog.get_logger()

# Create router
router = APIRouter()

# Initialize service
agent_service = AgentService()


@router.post("/process")
async def process_content(request: DomainRequest):
    """Process {{ cookiecutter.domain_name }} content using the agent.
    
    Args:
        request: Processing request with content and metadata
        
    Returns:
        Processing result
    """
    try:
        logger.info(
            "Received {{ cookiecutter.domain_name }} processing request",
            content_length=len(request.content),
            source=request.source,
            language=request.language
        )
        
        result = await agent_service.process(
            content=request.content,
            metadata=request.metadata,
            options=request.options
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(
            "{{ cookiecutter.domain_name }} processing request failed",
            error=str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )


@router.post("/process-with-reflection")
async def process_with_reflection(request: DomainRequest):
    """Process {{ cookiecutter.domain_name }} content with reflection enabled.
    
    Args:
        request: Processing request with content and metadata
        
    Returns:
        Processing result with reflection
    """
    try:
        logger.info(
            "Received {{ cookiecutter.domain_name }} reflection processing request",
            content_length=len(request.content),
            source=request.source,
            language=request.language
        )
        
        result = await agent_service.process_with_reflection(
            content=request.content,
            metadata=request.metadata,
            options=request.options
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(
            "{{ cookiecutter.domain_name }} reflection processing failed",
            error=str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Reflection processing failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check for {{ cookiecutter.domain_name }} service.
    
    Returns:
        Service health status
    """
    try:
        health_result = await agent_service.health_check()
        
        if health_result["status"] == "healthy":
            return JSONResponse(content=health_result)
        else:
            return JSONResponse(
                status_code=503,
                content=health_result
            )
            
    except Exception as e:
        logger.error(
            "{{ cookiecutter.domain_name }} health check failed",
            error=str(e),
            exc_info=True
        )
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


@router.get("/schema")
async def get_workflow_schema():
    """Get the agent workflow schema.
    
    Returns:
        Workflow schema information
    """
    try:
        schema = agent_service.agent_builder.get_workflow_schema()
        return JSONResponse(content=schema)
        
    except Exception as e:
        logger.error(
            "Failed to get workflow schema",
            error=str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get schema: {str(e)}"
        ) 