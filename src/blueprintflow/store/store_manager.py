from uuid import uuid4

from blueprintflow.core.models.settings import BlueprintFlowSettings
from blueprintflow.core.models.tasks import (
    CreateAstractionTask,
    CreateCodeTask,
    CreateGuidelineTask,
    CreateLanguageContextTask,
    CreatePreferenceTask,
    CreateRuleTask,
    CreateSrcStructureTask,
    TaskStatusEnum,
)
from blueprintflow.llm.connector import LLMConnector
from blueprintflow.store.lancedb_handler import LanceDB
from blueprintflow.utils.xdg.data import UserData


class StoreManager:
    """High-level component managing database interactions for BlueprintFlow.

    This class orchestrates the creation, storage, and retrieval of entities and their
    relationships, ensuring seamless integration with BlueprintFlow's data workflows.
    It abstracts low-level database operations, providing a unified interface for
    data persistence and query execution.

    Attributes:
        lance_handler (LanceDB): Handler for interacting with the LanceDB vector store.
        settings (BlueprintFlowSettings): Configuration settings for BlueprintFlow.
    """

    def __init__(self, settings: BlueprintFlowSettings, user_data: UserData) -> None:
        """Initialize the StoreManager.

        Args:
            settings (BlueprintFlowSettings): Configuration settings for BlueprintFlow.
            user_data (UserData): User-specific data required for database
                initialization.

        Example:
            >>> from blueprintflow.core.settings import load_settings
            >>> settings = load_settings()
            >>> user_data = UserData()
            >>> store_manager = StoreManager(settings, user_data)
        """
        self.lance_handler = LanceDB(user_data)
        self.settings = settings
        self.llm_connector = LLMConnector(models=settings.models)

    def create(
        self,
        task: CreateLanguageContextTask
        | CreatePreferenceTask
        | CreateGuidelineTask
        | CreateRuleTask
        | CreateSrcStructureTask
        | CreateAstractionTask
        | CreateCodeTask,
    ) -> TaskStatusEnum:
        """Create a new record in the database from a task object.

        Takes a task object containing the data to be stored, optionally generates an
        embedding if not provided, and creates a corresponding record in the database.

        Args:
            task: A task object containing the data to be stored. Can be any of the
                supported task types representing different entities in the system.

        Returns:
            TaskStatusEnum: SUCCESS if the record was created successfully,
                        FAILURE otherwise.
        """
        if task.key is None:
            task.key = str(uuid4())
        if task.embedding is None:
            task.embedding = self.llm_connector.get_embedding(str(task))
        success = self.lance_handler.create_record(task.to_data_store_model())
        if not success:
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS
