"""
LLM Factory for creating language model instances.
"""

from typing import Protocol

from langchain_core.language_models import BaseLanguageModel

from app.infrastructure.config.config import get_openai_config
from app.infrastructure.llm.openai_service import OpenAIService
from app.application.interfaces.illm_service import ILLMService


class LLMFactory:
    @staticmethod
    def create_llm_service(llm_provider: str) -> ILLMService:

        if llm_provider == "openai":
            return OpenAIService()
        else:
            raise ValueError(f"LLM não suportado: {llm_provider}")