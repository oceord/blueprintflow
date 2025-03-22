from typing import NamedTuple

from pydantic import BaseModel


class KuzuProperty(NamedTuple):
    """A named tuple representing a property in a Kuzu node or relationship.

    Attributes:
        name (str): The name of the property.
        type (str): The data type of the property.
        default (str | None, optional): The default value of the property.
            Defaults to None.
    """

    name: str
    type: str
    default: str | None = None


class KuzuNode(BaseModel):
    """A model representing a node in the Kuzu database.

    Attributes:
        name (str): The name of the node.
        properties (list[KuzuProperty]): A list of properties associated with the node.
        primary_key (list[str]): A list of property names that form the primary key of
            the node.
    """

    name: str
    properties: list[KuzuProperty]
    primary_key: list[str]


class KuzuRelationship(BaseModel):
    """A model representing a relationship between nodes in the Kuzu database.

    Attributes:
        name (str): The name of the relationship.
        properties (list[KuzuProperty]): A list of properties associated with the
            relationship.
        from_node (str): The name of the source node in the relationship.
        to_node (str): The name of the target node in the relationship.
    """

    name: str
    properties: list[KuzuProperty]
    from_node: str
    to_node: str


KUZU_NODES = [
    KuzuNode(
        name="LanguageContext",
        properties=[
            KuzuProperty("n_id", "SERIAL"),
            KuzuProperty("name", "STRING"),
            KuzuProperty("description", "STRING"),
            KuzuProperty("context", "STRING"),
        ],
        primary_key=["n_id"],
    ),
    KuzuNode(
        name="Preference",
        properties=[
            KuzuProperty("n_id", "SERIAL"),
            KuzuProperty("name", "STRING"),
            KuzuProperty("description", "STRING"),
        ],
        primary_key=["n_id"],
    ),
    KuzuNode(
        name="Guideline",
        properties=[
            KuzuProperty("n_id", "SERIAL"),
            KuzuProperty("name", "STRING"),
            KuzuProperty("description", "STRING"),
        ],
        primary_key=["n_id"],
    ),
    KuzuNode(
        name="Rule",
        properties=[
            KuzuProperty("n_id", "SERIAL"),
            KuzuProperty("name", "STRING"),
            KuzuProperty("description", "STRING"),
            KuzuProperty("enforcement_level", "UINT8"),
        ],
        primary_key=["n_id"],
    ),
    KuzuNode(
        name="SourceStructure",
        properties=[
            KuzuProperty("n_id", "SERIAL"),
            KuzuProperty("name", "STRING"),
            KuzuProperty("type", "STRING"),
        ],
        primary_key=["n_id"],
    ),
]
KUZU_RELATIONSHIPS = [
    KuzuRelationship(
        name="PREFERS_TOOL",
        properties=[KuzuProperty("r_id", "SERIAL")],
        from_node="LanguageContext",
        to_node="Preference",
    ),
    KuzuRelationship(
        name="FOLLOWS_GUIDELINE",
        properties=[KuzuProperty("r_id", "SERIAL")],
        from_node="LanguageContext",
        to_node="Guideline",
    ),
    KuzuRelationship(
        name="ENFORCES_RULE",
        properties=[KuzuProperty("r_id", "SERIAL")],
        from_node="LanguageContext",
        to_node="Rule",
    ),
    KuzuRelationship(
        name="CONTAINS_STRUCTURE",
        properties=[KuzuProperty("r_id", "SERIAL")],
        from_node="LanguageContext",
        to_node="SourceStructure",
    ),
]
