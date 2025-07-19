"""
LLM Factory for creating language model instances.
"""

from typing import Protocol

from langchain_core.language_models import BaseLanguageModel

from app.infrastructure.config.config import get_openai_config
from app.infrastructure.llm.openai_service import OpenAIService


class LLMServiceProtocol(Protocol):
    """Protocol for LLM services."""
    
    def get_llm(self) -> BaseLanguageModel:
        """Get the language model instance."""
        ...


class LLMFactory:
    """Factory for creating LLM instances."""
    
    @staticmethod
    def create_openai_service() -> OpenAIService:
        """Create OpenAI service with configuration."""
        config = get_openai_config()
        return OpenAIService(
            api_key=config["api_key"],
            model=config["model"],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"]
        )
    
    @staticmethod
    def create_default_llm() -> BaseLanguageModel:
        """Create default LLM instance."""
        service = LLMFactory.create_openai_service()
        return service.get_llm() 