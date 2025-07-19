"""
Interfaces for LLM services.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Protocol

from langchain_core.language_models import BaseLanguageModel

class ILLMService(ABC):
    pass