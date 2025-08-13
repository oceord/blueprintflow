from litellm import embedding

from blueprintflow.core.models.settings import ModelConfig, ModelTaskEnum


class LLMConnector:
    """A connector class for interacting with Language Model (LLM) services.

    Handles embedding generation and model management based on predefined tasks.

    Attributes:
        models (dict[ModelTaskEnum, ModelConfig]): A dictionary mapping model tasks to
            their configurations.
    """

    def __init__(self, models: dict[ModelTaskEnum, ModelConfig]) -> None:
        """Initializes the LLMConnector with a dictionary of model configurations.

        Args:
            models (dict[ModelTaskEnum, ModelConfig]): A dictionary where keys are model
                task enums and values are the corresponding model configurations.
        """
        self.models = models

    def get_embedding(self, input_str: str) -> list[float]:
        """Generates an embedding for the provided input string.

        Args:
            input_str (str): The input string to generate an embedding for.

        Returns:
            list[float]: The generated embedding as a list of floats.
        """
        model = self.models[ModelTaskEnum.EMBEDDING]
        response = embedding(
            model=model.identifier,
            input=[input_str],
            api_base=model.api_base,
        )
        embedding_obj: list[float] = response.data[0].get("embedding")
        return embedding_obj
