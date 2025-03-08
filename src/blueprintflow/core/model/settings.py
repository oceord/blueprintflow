from enum import Enum
from typing import Any, ClassVar, Optional

from pydantic import BaseModel


class ModelTask(str, Enum):
    """Enumeration of supported LLM tasks.

    This enum defines the various tasks that an LLM can perform.
    Each member of the enum represents a specific task supported by the LLM.
    """

    chat = "chat"
    embedding = "embedding"
    function_calling = "function_calling"
    long_context = "long_context"
    question_answering = "question_answering"
    rag = "rag"
    summarization = "summarization"
    text_classification = "text_classification"


class ModelConfig(BaseModel):
    """Represents the configuration for an LLM model.

    Attributes:
        identifier (str): The unique identifier for the model.
        provider (str): The provider of the model.
        api_base (str): The base URL for the model's API.
    """

    identifier: str
    provider: str
    api_base: str


class BlueprintFlowSettings(BaseModel):
    """Singleton settings for BlueprintFlow.

    This class represents the settings for BlueprintFlow, ensuring that only
    one instance of the settings exists. It contains a dictionary of models,
    each associated with its configuration.

    Attributes:
        models (dict[ModelTask, ModelConfig]): A dictionary mapping model tasks to their
            configurations.
        _instance (ClassVar[Optional["BlueprintFlowSettings"]]): The singleton instance
            of BlueprintFlowSettings.
        initialized (ClassVar[bool]): A flag indicating whether the settings have been
            initialized.
    """

    models: dict[ModelTask, ModelConfig]

    _instance: ClassVar[Optional["BlueprintFlowSettings"]] = None
    initialized: ClassVar[bool] = False

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
        if not self.__class__.initialized:
            super().__init__(**data)
            self.__class__.initialized = True
