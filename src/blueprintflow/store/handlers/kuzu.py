from typing import Any

from kuzu import Connection, Database, PreparedStatement, QueryResult

from blueprintflow.core.models.store import (
    KUZU_NODES,
    KUZU_RELATIONSHIPS,
    KuzuNode,
    KuzuRelationship,
)
from blueprintflow.helpers.store import gen_cs_properties
from blueprintflow.helpers.xdg.data import UserData
from blueprintflow.store.handlers.stmt import (
    TMPL_CYPHER_CREATE_NODE_TABLE,
    TMPL_CYPHER_CREATE_REL_TABLE,
)


class KuzuHandler:
    """A handler for interacting with the Kuzu database.

    This class provides methods to initialize the database, create nodes and
    relationships, and execute queries. It manages both read-write and read-only
    connections to the database.

    Attributes:
        uri (str): The URI of the Kuzu database file.
        db_read_only (Database): A read-only instance of the Kuzu database.
        db_read_write (Database): A read-write instance of the Kuzu database.
    """

    def __init__(self, user_data: UserData) -> None:
        """Initialize the Kuzu database handler.

        Args:
            user_data (UserData): An instance of UserData containing the Kuzu database
                file path.

        Attributes:
            uri (str): The URI of the Kuzu database file.
            db_read_only (Database): A read-only instance of the Kuzu database.
            db_read_write (Database): A read-write instance of the Kuzu database.
        """
        self.uri = user_data.kuzu_file
        self.db_read_only = Database(self.uri, read_only=True, lazy_init=True)
        self.db_read_write = Database(self.uri, lazy_init=True)
        self._init_bpf_tables()

    def get_connection(self, *, read_only: bool = True) -> "Connection":
        """Get a connection to the Kuzu database.

        Args:
            read_only (bool, optional): If True, return a read-only connection.
                Defaults to True.

        Returns:
            Connection: A connection to the Kuzu database.

        Examples:
            >>> kuzu = Kuzu(user_data)
            >>> conn = kuzu.get_connection(read_only=False)
            >>> isinstance(conn, Connection)
            True
            >>> conn = kuzu.get_connection(read_only=True)
            >>> isinstance(conn, Connection)
            True
        """
        return Connection(self.db_read_only if read_only else self.db_read_write)

    def _init_bpf_tables(self) -> None:
        """Initialize BlueprintFlow tables in the Kuzu database.

        This method creates the necessary nodes and relationships in the Kuzu database
        based on the predefined KUZU_NODES and KUZU_RELATIONSHIPS.
        """
        conn = self.get_connection(read_only=False)
        for pending in KUZU_NODES:
            KuzuHandler.create_node_table(conn, pending)
        for pending in KUZU_RELATIONSHIPS:
            KuzuHandler.create_rel_table(conn, pending)

    @staticmethod
    def create_node_table(conn: Connection, node: KuzuNode) -> None:
        """Create a node in the Kuzu database.

        Args:
            conn (Connection): A connection to the Kuzu database.
            node (KuzuNode): An instance of KuzuNode containing the node definition.
        """
        query = TMPL_CYPHER_CREATE_NODE_TABLE.substitute(
            name=node.name,
            cs_properties=gen_cs_properties(node.properties),
            cs_primary_key=", ".join(node.primary_key),
        )
        KuzuHandler.execute(conn, query)

    @staticmethod
    def create_rel_table(conn: Connection, rel: KuzuRelationship) -> None:
        """Create a relationship table in the Kuzu database.

        Args:
            conn (Connection): A connection to the Kuzu database.
            rel (KuzuRelationship): An instance of KuzuRelationship containing the
                relationship definition.
        """
        query = TMPL_CYPHER_CREATE_REL_TABLE.substitute(
            name=rel.name,
            from_node=rel.from_node,
            to_node=rel.to_node,
            cs_properties=gen_cs_properties(rel.properties),
        )
        KuzuHandler.execute(conn, query)

    @staticmethod
    def execute(
        conn: Connection,
        query: str | PreparedStatement,
        parameters: dict[str, Any] | None = None,
    ) -> QueryResult:
        """Execute a query on the Kuzu database.

        Args:
            conn (Connection): A connection to the Kuzu database.
            query (str | PreparedStatement): The query to execute.
            parameters (dict[str, Any], optional): The parameters to pass to the query.
                Defaults to None.

        Returns:
            QueryResult: The result of the query execution.

        Raises:
            ValueError: If the query execution does not return a QueryResult object.
        """
        result = conn.execute(query, parameters)
        if isinstance(result, QueryResult):
            return result
        value_error_msg = "Kuzu did not return a QueryResult object"
        raise ValueError(value_error_msg)
