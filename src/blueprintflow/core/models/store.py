from enum import StrEnum

from pydantic import BaseModel


class DataStoreEnum(StrEnum):
    """Enumeration of supported data stores.

    This enum defines the names of the data stores used by BlueprintFlow.
    Each member of the enum represents a specific store.
    """

    KUZU = "kuzudb"
    LANCEDB = "lancedb"


class KuzuNodeTableNameEnum(StrEnum):
    """Enumeration of node table names in the Kuzu database."""

    GUIDELINE = "Guideline"
    LANG_CONTEXT = "LanguageContext"
    PREFERENCE = "Preference"
    RULE = "Rule"
    SRC_STRUCTURE = "SourceStructure"


class KuzuRelTableNameEnum(StrEnum):
    """Enumeration of relationship table names in the Kuzu database."""

    CONTAINS_STRUCTURE = "CONTAINS_STRUCTURE"
    ENFORCES_RULE = "ENFORCES_RULE"
    FOLLOWS_GUIDELINE = "FOLLOWS_GUIDELINE"
    PREFERS_TOOL = "PREFERS_TOOL"


class KuzuPropertyNameEnum(StrEnum):
    """Enumeration of property names used in the Kuzu database."""

    CONTEXT = "context"
    DESCRIPTION = "description"
    ENFORCEMENT_LEVEL = "enforcement_level"
    LANGUAGE = "language"
    NAME = "name"
    NODE_ID = "n_id"
    PATH = "path"
    REL_ID = "r_id"
    TYPE = "type"


class KuzuDataTypeEnum(StrEnum):
    """Enumeration of data types used in the Kuzu database."""

    SERIAL = "SERIAL"
    STRING = "STRING"
    UINT8 = "UINT8"


class KuzuMatchOpEnum(StrEnum):
    """Enumeration of match operations used in the Kuzu database."""

    EQUAL = "="


class KuzuMatchCondition(BaseModel):
    """A model representing a match condition for filtering nodes in the Kuzu database.

    Attributes:
        property (KuzuPropertyNameEnum): The name of the property to match against.
        operation (KuzuMatchOpEnum): The operation to perform for matching.
        value (str): The value to compare against the property.

    Examples:
        >>> match_condition = KuzuMatchCondition(
        ...     property=KuzuPropertyNameEnum.LANGUAGE,
        ...     operation=KuzuMatchOpEnum.EQUAL,
        ...     value="Python"
        ... )

        Failure example when trying to pass invalid values:

        >>> match_condition = KuzuMatchCondition(
        ...     property=KuzuPropertyNameEnum.LANGUAGE,
        ...     operation="INVALID_OP",
        ...     value="Python"
        ... )  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValidationError
    """

    property: KuzuPropertyNameEnum
    operation: KuzuMatchOpEnum
    value: str


class KuzuTableProperty(BaseModel):
    """A model representing a table property in a Kuzu node or relationship.

    Attributes:
        name (KuzuPropertyNameEnum): The name of the property.
        type (KuzuDataTypeEnum): The data type of the property.
        default (str, optional): The default value of the property.
            Defaults to None.

    Examples:
        >>> prop = KuzuTableProperty(
        ...     name=KuzuPropertyNameEnum.NODE_ID,
        ...     type=KuzuDataTypeEnum.SERIAL,
        ... )

        Failure example when trying to pass invalid values:

        >>> prop = KuzuTableProperty(
        ...     name=KuzuPropertyNameEnum.NAME,
        ...     type="NONEXISTENT_TYPE",
        ...     default="default_name",
        ... )  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValidationError
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

    Examples:
        >>> node_table = KuzuNodeTable(
        ...     name=KuzuNodeTableNameEnum.LANG_CONTEXT,
        ...     properties=[
        ...         KuzuTableProperty(
        ...             name=KuzuPropertyNameEnum.NODE_ID,
        ...             type=KuzuDataTypeEnum.SERIAL,
        ...         ),
        ...         KuzuTableProperty(
        ...             name=KuzuPropertyNameEnum.LANGUAGE,
        ...             type=KuzuDataTypeEnum.STRING,
        ...         ),
        ...     ],
        ...     primary_key=[KuzuPropertyNameEnum.NODE_ID],
        ... )

        Failure example when trying to pass invalid values:

        >>> node_table = KuzuNodeTable(
        ...     name="NONEXISTENT_NODE_TABLE",
        ...     properties=[
        ...         KuzuTableProperty(
        ...             name=KuzuPropertyNameEnum.NODE_ID,
        ...             type=KuzuDataTypeEnum.SERIAL,
        ...         ),
        ...         KuzuTableProperty(
        ...             name=KuzuPropertyNameEnum.LANGUAGE,
        ...             type=KuzuDataTypeEnum.STRING,
        ...         ),
        ...     ],
        ...     primary_key=[KuzuPropertyNameEnum.NODE_ID],
        ... )  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValidationError
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

    Examples:
        >>> rel_table = KuzuRelTable(
        ...     name=KuzuRelTableNameEnum.PREFERS_TOOL,
        ...     properties=[
        ...         KuzuTableProperty(
        ...             name=KuzuPropertyNameEnum.REL_ID,
        ...             type=KuzuDataTypeEnum.SERIAL,
        ...         ),
        ...     ],
        ...     from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        ...     to_node_table=KuzuNodeTableNameEnum.PREFERENCE,
        ... )

        Failure example when trying to pass invalid values:

        >>> rel_table = KuzuRelTable(
        ...     name="NONEXISTENT_REL_TABLE",
        ...     properties=[
        ...         KuzuTableProperty(
        ...             name=KuzuPropertyNameEnum.REL_ID,
        ...             type=KuzuDataTypeEnum.SERIAL,
        ...         ),
        ...     ],
        ...     from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        ...     to_node_table=KuzuNodeTableNameEnum.PREFERENCE,
        ... )  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValidationError
    """

    name: KuzuRelTableNameEnum
    properties: list[KuzuTableProperty]
    from_node_table: KuzuNodeTableNameEnum
    to_node_table: KuzuNodeTableNameEnum


class KuzuProperty(BaseModel):
    """A model representing a property in a Kuzu node or relationship.

    Attributes:
        name (KuzuPropertyNameEnum): The name of the property.
        value (str): The value of the property.

    Examples:
        >>> property = KuzuProperty(
        ...     name=KuzuPropertyNameEnum.NAME,
        ...     value="python"
        ... )

        Failure example when trying to pass invalid values:

        >>> property = KuzuProperty(
        ...     name="NONEXISTENT_PROPERTY",
        ...     value="python"
        ... )  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValidationError
    """

    name: KuzuPropertyNameEnum
    value: str


class KuzuNode(BaseModel):
    """A model representing a node in the Kuzu database.

    Attributes:
        table_name (KuzuNodeTableEnum): The name of the node table.
        properties (list[KuzuProperty]): A list of properties associated with the node.

    Examples:
        >>> node = KuzuNode(
        ...     table_name=KuzuNodeTableNameEnum.LANG_CONTEXT,
        ...     properties=[
        ...         KuzuProperty(name=KuzuPropertyNameEnum.NAME, value="python"),
        ...     ]
        ... )

        Failure example when trying to pass invalid values:

        >>> node = KuzuNode(
        ...     table_name="NONEXISTENT_NODE",
        ...     properties=[
        ...             KuzuProperty(
        ...             name=KuzuPropertyNameEnum.NAME,
        ...             value="python",
        ...         ),
        ...     ]
        ... )  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValidationError
    """

    table_name: KuzuNodeTableNameEnum
    properties: list[KuzuProperty]


class KuzuRel(BaseModel):
    """A model representing a relationship between nodes in the Kuzu database.

    Attributes:
        rel_name (KuzuRelTableEnum): The name of the relationship.
        from_node_table (KuzuNodeTableEnum): The name of the source node table in the
            relationship.
        to_node_table (KuzuNodeTableEnum): The name of the target node table in the
            relationship.
        properties (list[KuzuProperty], optional): A list of properties associated with
            the relationship. Defaults to None.
        from_match_conditions (list[KuzuMatchCondition]): A list of match conditions for
            the source node.
        to_match_conditions (list[KuzuMatchCondition]): A list of match conditions for
            the target node.

    Examples:
        >>> prefers_tool_relationship = KuzuRel(
        ...     rel_name=KuzuRelTableNameEnum.PREFERS_TOOL,
        ...     from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        ...     to_node_table=KuzuNodeTableNameEnum.PREFERENCE,
        ...     properties=None,
        ...     from_match_conditions=[
        ...         KuzuMatchCondition(
        ...             property=KuzuPropertyNameEnum.LANGUAGE,
        ...             operation=KuzuMatchOpEnum.EQUAL,
        ...             value="python",
        ...         )
        ...     ],
        ...     to_match_conditions=[
        ...         KuzuMatchCondition(
        ...             property=KuzuPropertyNameEnum.NAME,
        ...             operation=KuzuMatchOpEnum.EQUAL,
        ...             value="polars",
        ...         )
        ...     ],
        ... )

        Failure example when trying to pass invalid values:

        >>> prefers_tool_relationship = KuzuRel(
        ...     rel_name="NONEXISTENT_REL",
        ...     from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        ...     to_node_table=KuzuNodeTableNameEnum.PREFERENCE,
        ...     properties=None,
        ...     from_match_conditions=[
        ...         KuzuMatchCondition(
        ...             property=KuzuPropertyNameEnum.LANGUAGE,
        ...             operation=KuzuMatchOpEnum.EQUAL,
        ...             value="python",
        ...         )
        ...     ],
        ...     to_match_conditions=[
        ...         KuzuMatchCondition(
        ...             property=KuzuPropertyNameEnum.NAME,
        ...             operation=KuzuMatchOpEnum.EQUAL,
        ...             value="polars",
        ...         )
        ...     ],
        ... )  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValidationError
    """

    rel_name: KuzuRelTableNameEnum
    from_node_table: KuzuNodeTableNameEnum
    to_node_table: KuzuNodeTableNameEnum
    properties: list[KuzuProperty] | None = None
    from_match_conditions: list[KuzuMatchCondition]
    to_match_conditions: list[KuzuMatchCondition]


KUZU_NODE_TABLES = [
    KuzuNodeTable(
        name=KuzuNodeTableNameEnum.LANG_CONTEXT,
        properties=[
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.NODE_ID,
                type=KuzuDataTypeEnum.SERIAL,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.LANGUAGE,
                type=KuzuDataTypeEnum.STRING,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.CONTEXT,
                type=KuzuDataTypeEnum.STRING,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.DESCRIPTION,
                type=KuzuDataTypeEnum.STRING,
            ),
        ],
        primary_key=[KuzuPropertyNameEnum.NODE_ID],
    ),
    KuzuNodeTable(
        name=KuzuNodeTableNameEnum.PREFERENCE,
        properties=[
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.NODE_ID,
                type=KuzuDataTypeEnum.SERIAL,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.NAME,
                type=KuzuDataTypeEnum.STRING,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.DESCRIPTION,
                type=KuzuDataTypeEnum.STRING,
            ),
        ],
        primary_key=[KuzuPropertyNameEnum.NODE_ID],
    ),
    KuzuNodeTable(
        name=KuzuNodeTableNameEnum.GUIDELINE,
        properties=[
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.NODE_ID,
                type=KuzuDataTypeEnum.SERIAL,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.NAME,
                type=KuzuDataTypeEnum.STRING,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.DESCRIPTION,
                type=KuzuDataTypeEnum.STRING,
            ),
        ],
        primary_key=[KuzuPropertyNameEnum.NODE_ID],
    ),
    KuzuNodeTable(
        name=KuzuNodeTableNameEnum.RULE,
        properties=[
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.NODE_ID,
                type=KuzuDataTypeEnum.SERIAL,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.NAME,
                type=KuzuDataTypeEnum.STRING,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.DESCRIPTION,
                type=KuzuDataTypeEnum.STRING,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.ENFORCEMENT_LEVEL,
                type=KuzuDataTypeEnum.UINT8,
            ),
        ],
        primary_key=[KuzuPropertyNameEnum.NODE_ID],
    ),
    KuzuNodeTable(
        name=KuzuNodeTableNameEnum.SRC_STRUCTURE,
        properties=[
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.NODE_ID,
                type=KuzuDataTypeEnum.SERIAL,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.PATH,
                type=KuzuDataTypeEnum.STRING,
            ),
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.DESCRIPTION,
                type=KuzuDataTypeEnum.STRING,
            ),
        ],
        primary_key=[KuzuPropertyNameEnum.NODE_ID],
    ),
]

KUZU_RELATIONSHIP_TABLES = [
    KuzuRelTable(
        name=KuzuRelTableNameEnum.PREFERS_TOOL,
        properties=[
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.REL_ID,
                type=KuzuDataTypeEnum.SERIAL,
            )
        ],
        from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        to_node_table=KuzuNodeTableNameEnum.PREFERENCE,
    ),
    KuzuRelTable(
        name=KuzuRelTableNameEnum.FOLLOWS_GUIDELINE,
        properties=[
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.REL_ID,
                type=KuzuDataTypeEnum.SERIAL,
            )
        ],
        from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        to_node_table=KuzuNodeTableNameEnum.GUIDELINE,
    ),
    KuzuRelTable(
        name=KuzuRelTableNameEnum.ENFORCES_RULE,
        properties=[
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.REL_ID,
                type=KuzuDataTypeEnum.SERIAL,
            )
        ],
        from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        to_node_table=KuzuNodeTableNameEnum.RULE,
    ),
    KuzuRelTable(
        name=KuzuRelTableNameEnum.CONTAINS_STRUCTURE,
        properties=[
            KuzuTableProperty(
                name=KuzuPropertyNameEnum.REL_ID,
                type=KuzuDataTypeEnum.SERIAL,
            )
        ],
        from_node_table=KuzuNodeTableNameEnum.LANG_CONTEXT,
        to_node_table=KuzuNodeTableNameEnum.SRC_STRUCTURE,
    ),
]
