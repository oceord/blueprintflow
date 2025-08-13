from enum import StrEnum
from typing import Any, ClassVar

from pydantic import BaseModel


class ModelTaskEnum(StrEnum):
    """Enumeration of supported LLM tasks.

    This enum defines the various tasks that an LLM can perform.
    Each member of the enum represents a specific task supported by the LLM.
    """

    CHAT = "chat"
    EMBEDDING = "embedding"
    FUNCTION_CALLING = "function_calling"
    LONG_CONTEXT = "long_context"
    QUESTION_ANSWERING = "question_answering"
    RAG = "rag"
    SUMMARIZATION = "summarization"
    TEXT_CLASSIFICATION = "text_classification"
    TEXT_EXTRACTION = "text_extraction"
    THINKING = "thinking"


class ModelConfig(BaseModel):
    """Represents the configuration for an LLM.

    Attributes:
        provider (str): The provider of the model.
        identifier (str): The unique identifier for the model.
        api_base (str): The base URL for the model's API.
    """

    provider: str
    identifier: str
    api_base: str


class BlueprintFlowSettings(BaseModel):
    """Singleton settings for BlueprintFlow.

    This class represents the settings for BlueprintFlow, ensuring that only
    one instance of the settings exists. It contains a dictionary of models,
    each associated with its configuration.

    Attributes:
        models (dict[ModelTask, ModelConfig]): A dictionary mapping model tasks to their
            configurations.
        _instance (BlueprintFlowSettings | None): The singleton instance
            of BlueprintFlowSettings.
        _initialized (bool): A flag indicating whether the settings have been
            initialized.
    """

    chat_model: ModelConfig
    embedding_model: ModelConfig
    function_calling_model: ModelConfig
    long_context_model: ModelConfig
    question_answering_model: ModelConfig
    rag_model: ModelConfig
    summarization_model: ModelConfig
    text_classification_model: ModelConfig
    text_extraction_model: ModelConfig
    thinking_model: ModelConfig

    _instance: ClassVar["BlueprintFlowSettings | None"] = None
    _initialized: ClassVar[bool] = False

    def __new__(cls, *_: Any, **__: Any) -> "BlueprintFlowSettings":
        """Create a new instance of BlueprintFlowSettings if none exists.

        This method ensures that only one instance of BlueprintFlowSettings is created.
        If an instance already exists, it returns the existing instance.

        Returns:
            BlueprintFlowSettings: The singleton instance of BlueprintFlowSettings.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, /, **data: Any) -> None:
        """Initialize the BlueprintFlowSettings instance.

        This method initializes the BlueprintFlowSettings instance with the provided
        data. It ensures that the initialization only occurs once.

        Args:
            **data (Any): The data to initialize the settings.
        """
        if not self.__class__._initialized:  # noqa: SLF001
            super().__init__(**data)
            self.__class__._initialized = True  # noqa: SLF001
