"""
Configuration settings for {{ cookiecutter.project_name }}.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str = "gpt-4o-mini"  
    OPENAI_TEMPERATURE: float = 0.2
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


if __name__ == "__main__":
    print("Configurações carregadas:") 