"""
Interfaces for LLM services.
"""

from typing import Any, Dict, Optional, Protocol

from langchain_core.language_models import BaseLanguageModel


class ILLMService(Protocol):
    """Interface for LLM services."""
    
    def get_llm(self) -> BaseLanguageModel:
        """Get the language model instance.
        
        Returns:
            Language model instance
        """
        ...
    
    def get_streaming_llm(self) -> BaseLanguageModel:
        """Get streaming language model instance.
        
        Returns:
            Streaming language model instance
        """
        ...


class IAgentService(Protocol):
    """Interface for agent services."""
    
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
        ...
    
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
        ...


class IConfigurationService(Protocol):
    """Interface for configuration services."""
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration.
        
        Returns:
            LLM configuration dictionary
        """
        ...
    
    def get_agent_config(self) -> Dict[str, Any]:
        """Get agent configuration.
        
        Returns:
            Agent configuration dictionary
        """
        ...
    
    def is_reflection_enabled(self) -> bool:
        """Check if reflection is enabled.
        
        Returns:
            True if reflection is enabled
        """
        ... 