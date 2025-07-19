import structlog
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI

logger = structlog.get_logger()
from app.infrastructure.config.config import settings

class OpenAIService:
    """Service for OpenAI language models."""
    def __init__(self):
        self.client = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL_NAME,
            temperature=settings.OPENAI_TEMPERATURE
        )