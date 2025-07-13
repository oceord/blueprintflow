from enum import StrEnum
from typing import NamedTuple

from pydantic import BaseModel


class DataStoreEnum(StrEnum):
    """Enumeration of supported data stores.

    This enum defines the names of the data stores used by BlueprintFlow.
    Each member of the enum represents a specific store.
    """

    LANCEDB = "lancedb"
    KUZU = "kuzudb"


class KuzuNodeTableNameEnum(StrEnum):
    """Enumeration of node table names in the Kuzu database."""

    LANG_CONTEXT = "LanguageContext"
    PREF = "Preference"
    GUIDELINE = "Guideline"
    RULE = "Rule"
    SRC_STRUCTURE = "SourceStructure"


class KuzuRelTableNameEnum(StrEnum):
    """Enumeration of relationship table names in the Kuzu database."""

    PREFERS_TOOL = "PREFERS_TOOL"
    FOLLOWS_GUIDELINE = "FOLLOWS_GUIDELINE"
    ENFORCES_RULE = "ENFORCES_RULE"
    CONTAINS_STRUCTURE = "CONTAINS_STRUCTURE"


class KuzuDataTypeEnum(StrEnum):
    """Enumeration of data types used in the Kuzu database."""

    SERIAL = "SERIAL"
    STRING = "STRING"
    UINT8 = "UINT8"


class KuzuPropertyNameEnum(StrEnum):
    """Enumeration of property names used in the Kuzu database."""

    NODE_ID = "n_id"
    LANGUAGE = "language"
    CONTEXT = "context"
    DESCRIPTION = "description"
    NAME = "name"
    ENFORCEMENT_LEVEL = "enforcement_level"
    TYPE = "type"
    REL_ID = "r_id"


class KuzuMatchOpEnum(StrEnum):
    """Enumeration of match operations used in the Kuzu database."""

    EQUAL = "="


class KuzuTableProperty(NamedTuple):
    """A named tuple representing a table property in a Kuzu node or relationship.

    Attributes:
        name (KuzuPropertyNameEnum): The name of the property.
        type (KuzuDataTypeEnum): The data type of the property.
        default (str | None, optional): The default value of the property.
            Defaults to None.
    """

    name: KuzuPropertyNameEnum
    type: KuzuDataTypeEnum
    default: str | None = None


class KuzuNodeTable(BaseModel):
    """A model representing a node table in the Kuzu database.

    Attributes:
        name (KuzuNodeTableEnum): The name of the node table.
        properties (list[KuzuTableProperty]): A list of properties associated with the
            node.
        primary_key (list[KuzuPropertyNameEnum]): A list of property names that form
            the primary key of the node.
    """

    name: KuzuNodeTableNameEnum
    properties: list[KuzuTableProperty]
    primary_key: list[KuzuPropertyNameEnum]


class KuzuRelTable(BaseModel):
    """A model representing a relationship table between nodes in the Kuzu database.

    Attributes:
        name (KuzuRelTableEnum): The name of the relationship.
        properties (list[KuzuTableProperty]): A list of properties associated with the
            relationship.
        from_node_table (KuzuNodeTableEnum): The name of the source table node in the
            relationship.
        to_node_table (KuzuNodeTableEnum): The name of the target table node in the
            relationship.
    """

    name: KuzuRelTableNameEnum
    properties: list[KuzuTableProperty]
    from_node_table: KuzuNodeTableNameEnum
    to_node_table: KuzuNodeTableNameEnum


class KuzuProperty(NamedTuple):
    """A named tuple representing a property in a Kuzu node or relationship.

    Attributes:
        name (KuzuPropertyNameEnum): The name of the property.
        value (str): The value of the property.
    """

    name: KuzuPropertyNameEnum
    value: str


class KuzuNode(BaseModel):
    """A model representing a node in the Kuzu database.

    Attributes:
        table_name (KuzuNodeTableEnum): The name of the node table.
        properties (list[KuzuProperty]): A list of properties associated with the node.
    """

    table_name: KuzuNodeTableNameEnum
    properties: list[KuzuProperty]


class KuzuMatchCondition(BaseModel):
    """A model representing a match condition for filtering nodes in the Kuzu database.

    Attributes:
        property (KuzuPropertyNameEnum): The name of the property to match against.
        operation (KuzuMatchOpEnum): The operation to perform for matching.
        value (str): The value to compare against the property.
    """

    property: KuzuPropertyNameEnum
    operation: KuzuMatchOpEnum
    value: str


class KuzuRel(BaseModel):
    """A model representing a relationship between nodes in the Kuzu database.

    Attributes:
        rel_name (KuzuRelTableEnum): The name of the relationship.
        from_node_table (KuzuNodeTableEnum): The name of the source node table in the
            relationship.
        to_node_table (KuzuNodeTableEnum): The name of the target node table in the
            relationship.
        properties (list[KuzuProperty] | None): A list of properties associated with
            the relationship.
        from_match_conditions (list[KuzuMatchCondition]): A list of match conditions for
            the source node.
        to_match_conditions (list[KuzuMatchCondition]): A list of match conditions for
            the target node.
    """

    rel_name: KuzuRelTableNameEnum
    from_node_table: KuzuNodeTableNameEnum
    to_node_table: KuzuNodeTableNameEnum
    properties: list[KuzuProperty] | None
    from_match_conditions: list[KuzuMatchCondition]
    to_match_conditions: list[KuzuMatchCondition]


KUZU_NODE_TABLES = [
    KuzuNodeTable(
        name=KuzuNodeTableNameEnum.LANG_CONTEXT,
        properties=[
            KuzuTableProperty(KuzuPropertyNameEnum.NODE_ID, KuzuDataTypeEnum.SERIAL),
            KuzuTableProperty(KuzuPropertyNameEnum.LANGUAGE, KuzuDataTypeEnum.STRING),
            KuzuTableProperty(KuzuPropertyNameEnum.CONTEXT, KuzuDataTypeEnum.STRING),
            KuzuTableProperty(
                KuzuPropertyNameEnum.DESCRIPTION, KuzuDataTypeEnum.STRING
            ),
        ],
        primary_key=[KuzuPropertyNameEnum.NODE_ID],
    ),
    KuzuNodeTable(
        name=KuzuNodeTableNameEnum.PREF,
        properties=[
            KuzuTableProperty(KuzuPropertyNameEnum.NODE_ID, KuzuDataTypeEnum.SERIAL),
            KuzuTableProperty(KuzuPropertyNameEnum.NAME, KuzuDataTypeEnum.STRING),
            KuzuTableProperty(
                KuzuPropertyNameEnum.DESCRIPTION, KuzuDataTypeEnum.STRING
            ),
        ],
        primary_key=[KuzuPropertyNameEnum.NODE_ID],
    ),
    KuzuNodeTable(
        name=KuzuNodeTableNameEnum.GUIDELINE,
        properties=[
            KuzuTableProperty(KuzuPropertyNameEnum.NODE_ID, KuzuDataTypeEnum.SERIAL),
            KuzuTableProperty(KuzuPropertyNameEnum.NAME, KuzuDataTypeEnum.STRING),
            KuzuTableProperty(
                KuzuPropertyNameEnum.DESCRIPTION, KuzuDataTypeEnum.STRING
            ),
        ],
        primary_key=[KuzuPropertyNameEnum.NODE_ID],
    ),
    KuzuNodeTable(
        name=KuzuNodeTableNameEnum.RULE,
        properties=[
            KuzuTableProperty(KuzuPropertyNameEnum.NODE_ID, KuzuDataTypeEnum.SERIAL),
            KuzuTableProperty(KuzuPropertyNameEnum.NAME, KuzuDataTypeEnum.STRING),
            KuzuTableProperty(
                KuzuPropertyNameEnum.DESCRIPTION, KuzuDataTypeEnum.STRING
            ),
            KuzuTableProperty(
                KuzuPropertyNameEnum.ENFORCEMENT_LEVEL,
                KuzuDataTypeEnum.UINT8,
            ),
        ],
        primary_key=[KuzuPropertyNameEnum.NODE_ID],
    ),
    KuzuNodeTable(
        name=KuzuNodeTableNameEnum.SRC_STRUCTURE,
        properties=[
            KuzuTableProperty(KuzuPropertyNameEnum.NODE_ID, KuzuDataTypeEnum.SERIAL),
            KuzuTableProperty(KuzuPropertyNameEnum.NAME, KuzuDataTypeEnum.STRING),
            KuzuTableProperty(KuzuPropertyNameEnum.TYPE, KuzuDataTypeEnum.STRING),
        ],
        primary_key=[KuzuPropertyNameEnum.NODE_ID],
    ),
]
KUZU_RELATIONSHIP_TABLES = [
    KuzuRelTable(
        name=KuzuRelTableNameEnum.PREFERS_TOOL,
        properties=[
            KuzuTableProperty(KuzuPropertyNameEnum.REL_ID, KuzuDataTypeEnum.SERIAL)
        ],
        from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        to_node_table=KuzuNodeTableNameEnum.PREF,
    ),
    KuzuRelTable(
        name=KuzuRelTableNameEnum.FOLLOWS_GUIDELINE,
        properties=[
            KuzuTableProperty(KuzuPropertyNameEnum.REL_ID, KuzuDataTypeEnum.SERIAL)
        ],
        from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        to_node_table=KuzuNodeTableNameEnum.GUIDELINE,
    ),
    KuzuRelTable(
        name=KuzuRelTableNameEnum.ENFORCES_RULE,
        properties=[
            KuzuTableProperty(KuzuPropertyNameEnum.REL_ID, KuzuDataTypeEnum.SERIAL)
        ],
        from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        to_node_table=KuzuNodeTableNameEnum.RULE,
    ),
    KuzuRelTable(
        name=KuzuRelTableNameEnum.CONTAINS_STRUCTURE,
        properties=[
            KuzuTableProperty(KuzuPropertyNameEnum.REL_ID, KuzuDataTypeEnum.SERIAL)
        ],
        from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        to_node_table=KuzuNodeTableNameEnum.SRC_STRUCTURE,
    ),
]
