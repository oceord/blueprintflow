from typing import NamedTuple

from pydantic import BaseModel


class KuzuTableProperty(NamedTuple):
    """A named tuple representing a table property in a Kuzu node or relationship.

    Attributes:
        name (str): The name of the property.
        type (str): The data type of the property.
        default (str | None, optional): The default value of the property.
            Defaults to None.
    """

    name: str
    type: str
    default: str | None = None


class KuzuNodeTable(BaseModel):
    """A model representing a node table in the Kuzu database.

    Attributes:
        name (str): The name of the node.
        properties (list[KuzuProperty]): A list of properties associated with the node.
        primary_key (list[str]): A list of property names that form the primary key of
            the node.
    """

    name: str
    properties: list[KuzuTableProperty]
    primary_key: list[str]


class KuzuRelationshipTable(BaseModel):
    """A model representing a relationship table between nodes in the Kuzu database.

    Attributes:
        name (str): The name of the relationship.
        properties (list[KuzuProperty]): A list of properties associated with the
            relationship.
        from_node_table (str): The name of the source table node in the relationship.
        to_node_table (str): The name of the target table node in the relationship.
    """

    name: str
    properties: list[KuzuTableProperty]
    from_node_table: str
    to_node_table: str


class KuzuProperty(NamedTuple):
    """A named tuple representing a property in a Kuzu node or relationship.

    Attributes:
        name (str): The name of the property.
        value (str): The value of the property.
    """

    name: str
    value: str


class KuzuNode(BaseModel):
    """A model representing a node in the Kuzu database.

    Attributes:
        table_name (str): The name of the node table.
        properties (list[KuzuProperty]): A list of properties associated with the node.
    """

    table_name: str
    properties: list[KuzuProperty]


class MatchCondition(BaseModel):
    """A model representing a match condition for filtering nodes in the Kuzu database.

    Attributes:
        property (str): The name of the property to match against.
        operation (str): The operation to perform for matching (e.g., "=").
        value (str): The value to compare against the property.
    """

    property: str
    operation: str
    value: str


class KuzuRelationship(BaseModel):
    """A model representing a relationship between nodes in the Kuzu database.

    Attributes:
        relationship_name (str): The name of the relationship.
        from_node_table (str): The name of the source node table in the relationship.
        to_node_table (str): The name of the target node table in the relationship.
        properties (list[KuzuProperty] | None): A list of properties associated with
            the relationship.
        from_match_conditions (list[MatchCondition]): A list of match conditions for
            the source node.
        to_match_conditions (list[MatchCondition]): A list of match conditions for
            the target node.
    """

    relationship_name: str
    from_node_table: str
    to_node_table: str
    properties: list[KuzuProperty] | None
    from_match_conditions: list[MatchCondition]
    to_match_conditions: list[MatchCondition]


KUZU_NODE_TABLES = [
    KuzuNodeTable(
        name="LanguageContext",
        properties=[
            KuzuTableProperty("n_id", "SERIAL"),
            KuzuTableProperty("language", "STRING"),
            KuzuTableProperty("context", "STRING"),
            KuzuTableProperty("description", "STRING"),
        ],
        primary_key=["n_id"],
    ),
    KuzuNodeTable(
        name="Preference",
        properties=[
            KuzuTableProperty("n_id", "SERIAL"),
            KuzuTableProperty("name", "STRING"),
            KuzuTableProperty("description", "STRING"),
        ],
        primary_key=["n_id"],
    ),
    KuzuNodeTable(
        name="Guideline",
        properties=[
            KuzuTableProperty("n_id", "SERIAL"),
            KuzuTableProperty("name", "STRING"),
            KuzuTableProperty("description", "STRING"),
        ],
        primary_key=["n_id"],
    ),
    KuzuNodeTable(
        name="Rule",
        properties=[
            KuzuTableProperty("n_id", "SERIAL"),
            KuzuTableProperty("name", "STRING"),
            KuzuTableProperty("description", "STRING"),
            KuzuTableProperty("enforcement_level", "UINT8"),
        ],
        primary_key=["n_id"],
    ),
    KuzuNodeTable(
        name="SourceStructure",
        properties=[
            KuzuTableProperty("n_id", "SERIAL"),
            KuzuTableProperty("name", "STRING"),
            KuzuTableProperty("type", "STRING"),
        ],
        primary_key=["n_id"],
    ),
]
KUZU_RELATIONSHIP_TABLES = [
    KuzuRelationshipTable(
        name="PREFERS_TOOL",
        properties=[KuzuTableProperty("r_id", "SERIAL")],
        from_node_table="LanguageContext",
        to_node_table="Preference",
    ),
    KuzuRelationshipTable(
        name="FOLLOWS_GUIDELINE",
        properties=[KuzuTableProperty("r_id", "SERIAL")],
        from_node_table="LanguageContext",
        to_node_table="Guideline",
    ),
    KuzuRelationshipTable(
        name="ENFORCES_RULE",
        properties=[KuzuTableProperty("r_id", "SERIAL")],
        from_node_table="LanguageContext",
        to_node_table="Rule",
    ),
    KuzuRelationshipTable(
        name="CONTAINS_STRUCTURE",
        properties=[KuzuTableProperty("r_id", "SERIAL")],
        from_node_table="LanguageContext",
        to_node_table="SourceStructure",
    ),
]
