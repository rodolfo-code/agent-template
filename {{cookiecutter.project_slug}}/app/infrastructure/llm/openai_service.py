"""
OpenAI service for language model integration.
"""

import structlog
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI

logger = structlog.get_logger()


class OpenAIService:
    """Service for OpenAI language models."""
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.1,
        max_tokens: int = 4000,
    ):
        """Initialize OpenAI service.
        
        Args:
            api_key: OpenAI API key
            model: Model name to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        logger.info(
            "Initializing OpenAI service",
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
    
    def get_llm(self) -> BaseLanguageModel:
        """Get configured ChatOpenAI instance."""
        return ChatOpenAI(
            api_key=self.api_key,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=60,
            max_retries=3,
        )
    
    def get_streaming_llm(self) -> BaseLanguageModel:
        """Get streaming ChatOpenAI instance."""
        return ChatOpenAI(
            api_key=self.api_key,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=60,
            max_retries=3,
            streaming=True,
        ) 