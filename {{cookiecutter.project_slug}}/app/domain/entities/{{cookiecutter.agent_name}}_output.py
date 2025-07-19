"""
{{ cookiecutter.agent_name }} output entities.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProcessingStatus(str, Enum):
    """Processing status enumeration."""
    
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentOutput(BaseModel):
    """Output model for {{ cookiecutter.agent_name }}."""
    
    id: UUID = Field(..., description="Processing ID")
    status: ProcessingStatus = Field(..., description="Processing status")
    result: Optional[str] = Field(None, description="Processing result")
    confidence_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence score of the result (0-1)"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Processing metadata"
    )
    execution_time: Optional[float] = Field(
        None,
        ge=0.0,
        description="Execution time in seconds"
    )
    tokens_used: Optional[int] = Field(
        None,
        ge=0,
        description="Number of tokens used"
    )
    error_message: Optional[str] = Field(
        None,
        description="Error message if processing failed"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    completed_at: Optional[datetime] = Field(
        None,
        description="Completion timestamp"
    )
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "completed",
                "result": "Processing completed successfully",
                "confidence_score": 0.95,
                "metadata": {"steps_executed": 3, "reflection_enabled": True},
                "execution_time": 2.34,
                "tokens_used": 150,
                "created_at": "2024-01-15T10:30:00Z",
                "completed_at": "2024-01-15T10:30:02Z"
            }
        }


class ProcessingStep(BaseModel):
    """Individual processing step within the agent workflow."""
    
    step_name: str = Field(..., description="Name of the processing step")
    status: ProcessingStatus = Field(..., description="Step status")
    input_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Input data for this step"
    )
    output_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Output data from this step"
    )
    execution_time: Optional[float] = Field(
        None,
        ge=0.0,
        description="Step execution time in seconds"
    )
    error_message: Optional[str] = Field(
        None,
        description="Error message if step failed"
    )
    started_at: datetime = Field(..., description="Step start time")
    completed_at: Optional[datetime] = Field(
        None,
        description="Step completion time"
    )


class DetailedAgentOutput(AgentOutput):
    """Detailed output model with step-by-step information."""
    
    steps: List[ProcessingStep] = Field(
        default_factory=list,
        description="List of processing steps"
    )
    reflection_notes: Optional[str] = Field(
        None,
        description="Agent reflection notes"
    )
    improvement_suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for improvement"
    ) 