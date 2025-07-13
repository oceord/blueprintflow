from typing import Any

from kuzu import Connection, Database, PreparedStatement, QueryResult

from blueprintflow.core.models.store import (
    KUZU_NODE_TABLES,
    KUZU_RELATIONSHIP_TABLES,
    KuzuNode,
    KuzuNodeTable,
    KuzuRel,
    KuzuRelTable,
)
from blueprintflow.helpers.cypher import (
    gen_cs_real_properties,
    gen_cs_table_properties,
    gen_match_condition,
)
from blueprintflow.helpers.xdg.data import UserData
from blueprintflow.store.handlers._stmts import (
    TMPL_CYPHER_CREATE_NODE,
    TMPL_CYPHER_CREATE_NODE_TABLE,
    TMPL_CYPHER_CREATE_REL_TABLE,
    TMPL_CYPHER_CREATE_RELATIONSHIP,
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
        self.uri = user_data.kuzu_path
        self._init_bpf_tables()

    def get_db(self, *, read_only: bool = True) -> Database:
        """Retrieve a database instance connected to the specified URI.

        Args:
            read_only (bool, optional): If True, the database is opened in read-only
                mode. Defaults to True.

        Returns:
            Database: An instance of the Database class connected to the URI specified
                in the object.
        """
        return Database(self.uri, read_only=read_only)

    def get_connection(self, *, read_only: bool = True) -> "Connection":
        """Get a connection to the Kuzu database.

        Args:
            read_only (bool, optional): If True, return a read-only connection.
                Defaults to True.

        Returns:
            Connection: A connection to the Kuzu database.

        Examples:
            >>> kuzu = Kuzu(user_data)
            >>> with kuzu.get_connection(read_only=False) as conn:
            >>>     isinstance(conn, Connection)
            True
            >>> with kuzu.get_connection(read_only=True) as conn:
            >>>     isinstance(conn, Connection)
            True
        """
        return Connection(self.get_db(read_only=read_only))

    def _init_bpf_tables(self) -> None:
        """Initialize BlueprintFlow tables in the Kuzu database.

        This method creates the necessary nodes and relationships in the Kuzu database
        based on the predefined KUZU_NODES and KUZU_RELATIONSHIPS.
        """
        for pending in KUZU_NODE_TABLES:
            self.create_table(pending)
        for pending in KUZU_RELATIONSHIP_TABLES:
            self.create_table(pending)

    def create_table(self, table: KuzuNodeTable | KuzuRelTable) -> None:
        """Create a node or relationship table in the Kuzu database.

        Args:
            table (KuzuNodeTable | KuzuRelTable): An instance of KuzuNodeTable or
                KuzuRelTable containing the table definition.
        """
        if isinstance(table, KuzuNodeTable):
            query = TMPL_CYPHER_CREATE_NODE_TABLE.substitute(
                name=table.name,
                cs_properties=gen_cs_table_properties(table.properties),
                cs_primary_key=", ".join(table.primary_key),
            )
        elif isinstance(table, KuzuRelTable):
            query = TMPL_CYPHER_CREATE_REL_TABLE.substitute(
                name=table.name,
                from_node_table=table.from_node_table,
                to_node_table=table.to_node_table,
                cs_properties=gen_cs_table_properties(table.properties),
            )
        with self.get_connection(read_only=False) as conn:
            KuzuHandler.execute(conn, query)

    def create_node(self, node: KuzuNode) -> None:
        """Create a node in the Kuzu database.

        This method generates a Cypher query to create a node with the specified
        properties and executes it against the Kuzu database.

        Args:
            node (KuzuNode): An instance of KuzuNode containing the node definition.
        """
        query = TMPL_CYPHER_CREATE_NODE.substitute(
            table_alias="n",
            table_name=node.table_name,
            cs_properties=gen_cs_real_properties(node.properties),
        )
        with self.get_connection(read_only=False) as conn:
            KuzuHandler.execute(conn, query)

    def create_relationship(self, rel: KuzuRel) -> None:
        """Create a relationship between nodes in the Kuzu database.

        This method generates a Cypher query to create a relationship with the specified
            properties and match conditions, then executes it against the Kuzu database.

        Args:
            rel (KuzuRel): An instance of KuzuRel containing the relationship
                definition.
        """
        from_alias = "n1"
        to_alias = "n2"
        rel_properties = gen_cs_real_properties(rel.properties, curlies=True)
        rel_properties_str = f" {rel_properties}" if rel_properties else rel_properties
        query = TMPL_CYPHER_CREATE_RELATIONSHIP.substitute(
            from_alias=from_alias,
            from_node_table=rel.from_node_table,
            to_alias=to_alias,
            to_node_table=rel.to_node_table,
            match_condition=gen_match_condition(
                from_alias,
                to_alias,
                rel.from_match_conditions,
                rel.to_match_conditions,
            ),
            rel=rel.rel_name,
            rel_properties=rel_properties_str,
        )
        with self.get_connection(read_only=False) as conn:
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
