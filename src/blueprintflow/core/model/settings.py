from enum import Enum
from typing import Any, ClassVar, Optional

from pydantic import BaseModel


class ModelTask(str, Enum):
    """Supported LLM tasks."""

    chat = "chat"
    embedding = "embedding"
    function_calling = "function_calling"
    long_context = "long_context"
    question_answering = "question_answering"
    rag = "rag"
    summarization = "summarization"
    text_classification = "text_classification"


class ModelConfig(BaseModel):
    """Represents Model configurations."""

    identifier: str
    provider: str
    api_base: str


class BlueprintFlowSettings(BaseModel):
    """BlueprintFlow singleton settings."""

    models: dict[ModelTask, ModelConfig]

    _instance: ClassVar[Optional["BlueprintFlowSettings"]] = None
    initialized: ClassVar[bool] = False

    def __new__(cls, *_: Any, **__: Any) -> "BlueprintFlowSettings":
        """Create a new instance of BlueprintFlowSettings if none exists.

        Returns:
            BlueprintFlowSettings: singleton instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, /, **data: Any) -> None:
        """Initialize BlueprintFlowSettings."""
        if not self.__class__.initialized:
            super().__init__(**data)
            self.__class__.initialized = True
