"""
Configuration settings for {{ cookiecutter.project_name }}.
"""

import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application Configuration
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # FastAPI Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    ENABLE_CORS: bool = True
    
    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "{{ cookiecutter.openai_model }}"
    OPENAI_TEMPERATURE: float = 0.1
    OPENAI_MAX_TOKENS: int = 4000
    
    # LangSmith Configuration (Optional)
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: Optional[str] = "{{ cookiecutter.project_slug }}"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    
    # Microsoft Bot Framework Configuration (Optional)
    MICROSOFT_APP_ID: Optional[str] = None
    MICROSOFT_APP_PASSWORD: Optional[str] = None
    # {{ cookiecutter.agent_name }} Specific Configuration
    {{ cookiecutter.agent_name.upper() }}_MAX_RETRIES: int = 3
    {{ cookiecutter.agent_name.upper() }}_TIMEOUT: int = 30
    {{ cookiecutter.agent_name.upper() }}_ENABLE_REFLECTION: bool = True
    
    # Additional Configuration
    MAX_CONCURRENT_REQUESTS: int = 10
    REQUEST_TIMEOUT: int = 60
    
    # Database Configuration (Optional)
    DATABASE_URL: Optional[str] = None
    
    # Redis Configuration (Optional)  
    REDIS_URL: Optional[str] = None

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "forbid"


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


def get_openai_config() -> dict:
    """Get OpenAI specific configuration."""
    settings = get_settings()
    return {
        "api_key": settings.OPENAI_API_KEY,
        "model": settings.OPENAI_MODEL,
        "temperature": settings.OPENAI_TEMPERATURE,
        "max_tokens": settings.OPENAI_MAX_TOKENS,
    }


def get_agent_config() -> dict:
    """Get {{ cookiecutter.agent_name }} specific configuration."""
    settings = get_settings()
    return {
        "max_retries": settings.{{ cookiecutter.agent_name.upper() }}_MAX_RETRIES,
        "timeout": settings.{{ cookiecutter.agent_name.upper() }}_TIMEOUT,
        "enable_reflection": settings.{{ cookiecutter.agent_name.upper() }}_ENABLE_REFLECTION,
    } 