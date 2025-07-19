"""
{{ cookiecutter.domain_name.title() }} domain entity.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEntity(BaseModel):
    """Main domain entity for {{ cookiecutter.domain_name }}."""
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    content: str = Field(..., description="Main content to be processed")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata"
    )
    source: Optional[str] = Field(None, description="Source of the content")
    language: str = Field(default="en", description="Content language")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Last update timestamp"
    )
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
        schema_extra = {
            "example": {
                "content": "Sample content for processing",
                "metadata": {"category": "sample", "priority": "high"},
                "source": "api",
                "language": "en"
            }
        }


class DomainRequest(BaseModel):
    """Request model for {{ cookiecutter.domain_name }} processing."""
    
    content: str = Field(..., description="Content to be processed")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata"
    )
    source: Optional[str] = Field(None, description="Source of the content")
    language: str = Field(default="en", description="Content language")
    options: Dict[str, Any] = Field(
        default_factory=dict,
        description="Processing options"
    )
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "content": "Sample content for processing",
                "metadata": {"category": "sample"},
                "source": "api",
                "language": "en",
                "options": {"enable_reflection": True}
            }
        } 