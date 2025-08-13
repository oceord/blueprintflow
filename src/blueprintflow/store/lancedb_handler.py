from pathlib import Path
from typing import cast

import lancedb
from lancedb import DBConnection
from lancedb.table import Table

from blueprintflow.core.models.data_store import (
    SCHEMAS,
    Abstraction,
    Code,
    Guideline,
    LanguageContext,
    Preference,
    QueryFilter,
    Rule,
    SourceStructure,
    TableNameEnum,
)
from blueprintflow.helpers.xdg.data import UserData


class LanceDB:
    """A handler for interacting with the LanceDB database.

    This class provides methods to initialize the database, create and manage
    records, and execute queries. It manages connections to the LanceDB database
    and handles all CRUD operations.

    Attributes:
        db_path (Path): Path to the LanceDB database directory.
        connection (Connection): Connection to the LanceDB database.

    Examples:
        >>> from blueprintflow.helpers.xdg.data import UserData
        >>> user_data = UserData()
        >>> db_handler = LanceDB(user_data)
    """

    def __init__(self, user_data: UserData) -> None:
        """Initialize the LanceDB database handler.

        Args:
            user_data (UserData): An instance of UserData containing the LanceDB
                database directory path.

        Examples:
            >>> from blueprintflow.helpers.xdg.data import UserData
            >>> user_data = UserData()
            >>> db_handler = LanceDB(user_data)
        """
        self.db_path = Path(user_data.lancedb_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.__init_tables()

    def __init_tables(self) -> None:
        """Initialize all required tables in the LanceDB database.

        This method checks the existing tables in the database and creates any tables
        defined in SCHEMAS that do not already exist.

        Note:
            This method is called automatically during initialization and does not need
            to be called manually.
        """
        existing_tables = self.get_connection().table_names()
        for table_name, schema in SCHEMAS.items():
            if table_name.value not in existing_tables:
                self.get_connection().create_table(table_name.value, schema=schema)

    def get_connection(self) -> DBConnection:
        """Get a connection to the LanceDB database.

        Establishes and returns a connection to the LanceDB database located at the
        path specified during initialization. The connection can be used to directly
        interact with the database if needed.

        Returns:
            DBConnection: A connection to the LanceDB database.

        Examples:
            >>> connection = db_handler.get_connection()  # doctest: +SKIP
            >>> tables = connection.table_names()  # doctest: +SKIP

        Note:
            Typically you don't need to call this method directly, as most operations
            are available through the LanceDB class methods. However, it's available
            if you need direct access to the database connection for advanced
            operations. Each call to this method creates a new connection object.
            Remember to properly close the connection if you're done with it, though
            Python's garbage collector will typically handle this.
        """
        return lancedb.connect(str(self.db_path))

    def get_table(self, table_name: TableNameEnum) -> Table:
        """Get a table from the database.

        Args:
            table_name (TableNameEnum): Name of the table to retrieve.

        Returns:
            Table: The requested LanceDB table.

        Examples:
            >>> from blueprintflow.core.models.store import TableNameEnum
            >>> table = db_handler.get_table(TableNameEnum.PREFERENCE)  # doctest: +SKIP

        Note:
            While you can use this method to get direct access to a table, most common
            operations are available through the higher-level methods of the LanceDB
            class. This method is provided for advanced usage or when you need
            operations not exposed by the higher-level API.
        """
        return self.get_connection().open_table(table_name.value)

    def query(self, query_filter: QueryFilter) -> list[dict]:
        """Query records from a table.

        Args:
            query_filter (QueryFilter): Query filter parameters.

        Returns:
            list[dict]: List of matching records.

        Examples:
            >>> from blueprintflow.core.models.store import QueryFilter, TableNameEnum
            >>> query_filter = QueryFilter(
            ...     table=TableNameEnum.PREFERENCE,
            ...     filter_conditions={"language_context_key": "python_data_001"},
            ...     limit=10,
            ... )
            >>> results = db_handler.query(query_filter)  # doctest: +SKIP
        """
        table = self.get_table(query_filter.table)
        if query_filter.filter_conditions:
            filter_str = self._gen_filter_str(query_filter.filter_conditions)
            results = (
                table.search().where(filter_str).limit(query_filter.limit).to_list()
            )
        else:
            results = table.search().limit(query_filter.limit).to_list()
        return cast("list[dict]", results)

    def get_by_key(self, table_name: TableNameEnum, record_key: str) -> dict | None:
        """Get a record by key.

        Args:
            table_name (TableNameEnum): Name of the table.
            record_key (str): record key.

        Returns:
            Optional[dict]: The record if found, None otherwise.

        Examples:
            >>> from blueprintflow.core.models.store import TableNameEnum
            >>> record = db_handler.get_by_key(  # doctest: +SKIP
            ...     TableNameEnum.PREFERENCE,
            ...     "pref_001",
            ... )
        """
        query = QueryFilter(
            table=table_name, filter_conditions={"key": record_key}, limit=1
        )
        results = self.query(query)
        return results[0] if results else None

    def create_record(
        self,
        record: LanguageContext
        | Preference
        | Guideline
        | Rule
        | SourceStructure
        | Code
        | Abstraction,
    ) -> bool:
        """Create a record in the appropriate table based on the model type.

        Args:
            record: The model object to create (one of the supported types)

        Returns:
            bool: True if successful.

        Raises:
            ValueError: If the record type is not recognized.

        Examples:
            >>> from blueprintflow.core.models.store import LanguageContext
            >>> lang_context = LanguageContext(
            ...     key="python_data_001",
            ...     language="python",
            ...     context="data",
            ...     description="Python for data science and analysis"
            ... )
            >>> db_handler.create_record(lang_context)  # doctest: +SKIP
        """
        match record:
            case LanguageContext():
                table_name = TableNameEnum.LANG_CONTEXT
            case Preference():
                table_name = TableNameEnum.PREFERENCE
            case Guideline():
                table_name = TableNameEnum.GUIDELINE
            case Rule():
                table_name = TableNameEnum.RULE
            case SourceStructure():
                table_name = TableNameEnum.SRC_STRUCTURE
            case Code():
                table_name = TableNameEnum.CODE
            case Abstraction():
                table_name = TableNameEnum.ABSTRACTION
        table = self.get_table(table_name)
        data = record.model_dump(exclude_none=True)
        table.add([data])
        return True

    def update_record(
        self, table_name: TableNameEnum, record_key: str, updates: dict
    ) -> bool:
        """Update a record.

        Args:
            table_name (TableNameEnum): Name of the table.
            record_key (str): record key to update.
            updates (dict): Fields to update.

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            >>> from blueprintflow.core.models.store import TableNameEnum
            >>> updates = {
            ...     "priority": 10,
            ...     "tags": ["dataframe", "performance"]
            ... }
            >>> db_handler.update_record(  # doctest: +SKIP
            ...     TableNameEnum.PREFERENCE,
            ...     "prf_001",
            ...     updates
            ... )
        """
        table = self.get_table(table_name)
        existing = self.get_by_key(table_name, record_key)
        if not existing:
            return False
        existing.update(updates)
        table.delete(f"key = '{record_key}'")
        table.add([existing])
        return True

    def delete_record(self, table_name: TableNameEnum, record_key: str) -> bool:
        """Delete a record.

        Args:
            table_name (TableNameEnum): Name of the table.
            record_key (str): record key to delete.

        Returns:
            bool: True if successful.

        Examples:
            >>> from blueprintflow.core.models.store import TableNameEnum
            >>> db_handler.delete_record(  # doctest: +SKIP
            ...     TableNameEnum.PREFERENCE,
            ...     "pref_001",
            ... )
        """
        table = self.get_table(table_name)
        table.delete(f"key = '{record_key}'")
        return True

    def search_vector(
        self,
        table_name: TableNameEnum,
        embedding: list[float],
        limit: int = 10,
        filter_conditions: dict | None = None,
    ) -> list[dict]:
        """Perform vector similarity search.

        Args:
            table_name (TableNameEnum): Name of the table to search.
            embedding (list[float]): Query embedding vector.
            limit (int): Maximum number of results.
            filter_conditions (dict, optional): Additional filter conditions.

        Returns:
            list[dict]: List of similar records.

        Examples:
            >>> from blueprintflow.core.models.store import TableNameEnum
            >>> embedding = [0.1, 0.2, 0.3, ...]
            >>> results = db_handler.vector_search(  # doctest: +SKIP
            ...     table_name=TableNameEnum.CODE,
            ...     embedding=embedding,
            ...     limit=5,
            ...     filter_conditions={"language_context_key": "python_data_001"}
            ... )
        """
        table = self.get_table(table_name)
        query = table.search(embedding).limit(limit)
        if filter_conditions:
            filter_str = self._gen_filter_str(filter_conditions)
            query = query.where(filter_str)
        return cast("list[dict]", query.to_list())

    @staticmethod
    def _gen_filter_str(filter_conditions: dict) -> str:
        filters = (
            f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}"
            for key, value in filter_conditions.items()
        )
        return " AND ".join(filters)
