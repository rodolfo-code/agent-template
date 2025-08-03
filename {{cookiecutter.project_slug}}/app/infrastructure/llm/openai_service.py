import logging
from app.application.interfaces.illm_service import ILLMService
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)
from app.infrastructure.config.config import settings

class OpenAIService(ILLMService):
    """Service for OpenAI language models."""
    def __init__(self):
        self.client = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL_NAME,
            temperature=settings.OPENAI_TEMPERATURE
        )