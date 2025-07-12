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
        from_node (str): The name of the source node in the relationship.
        to_node (str): The name of the target node in the relationship.
    """

    name: str
    properties: list[KuzuTableProperty]
    from_node: str
    to_node: str


KUZU_NODE_TABLES = [
    KuzuNodeTable(
        name="LanguageContext",
        properties=[
            KuzuTableProperty("n_id", "SERIAL"),
            KuzuTableProperty("name", "STRING"),
            KuzuTableProperty("description", "STRING"),
            KuzuTableProperty("context", "STRING"),
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
        from_node="LanguageContext",
        to_node="Preference",
    ),
    KuzuRelationshipTable(
        name="FOLLOWS_GUIDELINE",
        properties=[KuzuTableProperty("r_id", "SERIAL")],
        from_node="LanguageContext",
        to_node="Guideline",
    ),
    KuzuRelationshipTable(
        name="ENFORCES_RULE",
        properties=[KuzuTableProperty("r_id", "SERIAL")],
        from_node="LanguageContext",
        to_node="Rule",
    ),
    KuzuRelationshipTable(
        name="CONTAINS_STRUCTURE",
        properties=[KuzuTableProperty("r_id", "SERIAL")],
        from_node="LanguageContext",
        to_node="SourceStructure",
    ),
]
