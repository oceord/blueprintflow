from typing import Literal, cast, overload
from uuid import uuid4

from blueprintflow.core.models.data_store import (
    Abstraction,
    Code,
    Guideline,
    LanguageContext,
    Preference,
    Rule,
    SourceStructure,
    TableNameEnum,
)
from blueprintflow.core.models.settings import BlueprintFlowSettings
from blueprintflow.core.models.tasks import (
    CreateTaskProtocol,
    TaskStatusEnum,
    TModel_co,
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
        self, task: CreateTaskProtocol[TModel_co]
    ) -> tuple[TaskStatusEnum, TModel_co | None]:
        """Create a new record in the database from a task object.

        Takes a task object containing the data to be stored, optionally generates a key
        and embedding if not provided, and creates a corresponding record in the
        database.

        Args:
            task: A task object containing the data to be stored. Can be any of the
                supported task types.

        Returns:
            tuple:
                A tuple where the first element is the status of the operation, and the
                second element is the created model instance if successful, or None if
                the operation failed.
        """
        if task.key is None:
            task.key = str(uuid4())
        if task.embedding is None:
            task.embedding = self.llm_connector.get_embedding(task.as_text_features())
        data_store_model = task.to_data_store_model()
        success = self.lance_handler.create_record(data_store_model)
        if not success:
            return TaskStatusEnum.FAILURE, None
        return TaskStatusEnum.SUCCESS, data_store_model

    @overload
    def search_similar(
        self,
        table_name: Literal[TableNameEnum.LANG_CONTEXT],
        limit: int = 10,
        filter_conditions: dict | None = None,
        query_text: str | None = None,
        embedding: list[float] | None = None,
    ) -> tuple[TaskStatusEnum, list[LanguageContext]]: ...

    @overload
    def search_similar(
        self,
        table_name: Literal[TableNameEnum.PREFERENCE],
        limit: int = 10,
        filter_conditions: dict | None = None,
        query_text: str | None = None,
        embedding: list[float] | None = None,
    ) -> tuple[TaskStatusEnum, list[Preference]]: ...

    @overload
    def search_similar(
        self,
        table_name: Literal[TableNameEnum.RULE],
        limit: int = 10,
        filter_conditions: dict | None = None,
        query_text: str | None = None,
        embedding: list[float] | None = None,
    ) -> tuple[TaskStatusEnum, list[Rule]]: ...

    @overload
    def search_similar(
        self,
        table_name: Literal[TableNameEnum.GUIDELINE],
        limit: int = 10,
        filter_conditions: dict | None = None,
        query_text: str | None = None,
        embedding: list[float] | None = None,
    ) -> tuple[TaskStatusEnum, list[Guideline]]: ...

    @overload
    def search_similar(
        self,
        table_name: Literal[TableNameEnum.SRC_STRUCTURE],
        limit: int = 10,
        filter_conditions: dict | None = None,
        query_text: str | None = None,
        embedding: list[float] | None = None,
    ) -> tuple[TaskStatusEnum, list[SourceStructure]]: ...

    @overload
    def search_similar(
        self,
        table_name: Literal[TableNameEnum.ABSTRACTION],
        limit: int = 10,
        filter_conditions: dict | None = None,
        query_text: str | None = None,
        embedding: list[float] | None = None,
    ) -> tuple[TaskStatusEnum, list[Abstraction]]: ...

    @overload
    def search_similar(
        self,
        table_name: Literal[TableNameEnum.CODE],
        limit: int = 10,
        filter_conditions: dict | None = None,
        query_text: str | None = None,
        embedding: list[float] | None = None,
    ) -> tuple[TaskStatusEnum, list[Code]]: ...

    @overload
    def search_similar(
        self,
        table_name: TableNameEnum,
        limit: int = 10,
        filter_conditions: dict | None = None,
        query_text: str | None = None,
        embedding: list[float] | None = None,
    ) -> tuple[
        TaskStatusEnum,
        list[LanguageContext]
        | list[Preference]
        | list[Rule]
        | list[Guideline]
        | list[SourceStructure]
        | list[Abstraction]
        | list[Code],
    ]: ...

    def search_similar(
        self,
        table_name: TableNameEnum,
        limit: int = 10,
        filter_conditions: dict | None = None,
        query_text: str | None = None,
        embedding: list[float] | None = None,
    ) -> tuple[
        TaskStatusEnum,
        list[LanguageContext]
        | list[Preference]
        | list[Rule]
        | list[Guideline]
        | list[SourceStructure]
        | list[Abstraction]
        | list[Code],
    ]:
        """Search for similar records in the specified table.

        Args:
            table_name (TableNameEnum):
                The name of the table to search in. Must be a member of the
                `TableNameEnum` enumeration.
            limit (int, optional):
                The maximum number of records to return. Defaults to 10.
            filter_conditions (dict | None, optional):
                A dictionary of filter conditions to apply to the search query.
                If provided, only records matching these conditions will be returned.
                Defaults to None.
            query_text (str | None, optional):
                The text to search for in the vector store. If provided and no embedding
                is specified, an embedding will be generated from this text.
                Defaults to None.
            embedding (list[float] | None, optional):
                An embedding vector for the search. If not provided, one will be
                generated from the `query_text` if available. Defaults to None.

        Returns:
            tuple:
                A tuple containing `TaskStatusEnum` indicating the success or failure of
                the operation and a list of data_store model objects.

        Raises:
            ValueError:
                If both `query_text` and `embedding` are None, as at least one is r
                equired for the search.
        """
        if query_text is None and embedding is None:
            msg = "Arguments query_text and embedding cannot be both None"
            raise ValueError(msg)
        if query_text is not None and embedding is None:
            embedding = self.llm_connector.get_embedding(query_text)
        model_instances = self.lance_handler.search_vector(
            table_name=table_name,
            embedding=cast("list[float]", embedding),
            limit=limit,
            filter_conditions=filter_conditions,
        )
        return TaskStatusEnum.SUCCESS, model_instances
