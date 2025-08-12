from enum import StrEnum

import pyarrow as pa
from pydantic import BaseModel


class TableNameEnum(StrEnum):
    """Enumeration of table names in the LanceDB database."""

    GUIDELINE = "guidelines"
    LANG_CONTEXT = "language_contexts"
    PREFERENCE = "preferences"
    RULE = "rules"
    SRC_STRUCTURE = "source_structures"
    CODE = "code"
    ABSTRACTION = "abstractions"


class LanguageContext(BaseModel):
    """A model representing a language context in LanceDB.

    Attributes:
        key (str): Key identifier for the language context.
        language (str): The programming language (e.g., "python", "javascript").
        context (str): The context or domain (e.g., "data", "web", "ml").
        description (str): A detailed description of the language context.
        embedding (list[float], optional): Vector embedding for similarity search.

    Examples:
        >>> lang_context = LanguageContext(
        ...     key="python_data_001",
        ...     language="python",
        ...     context="data",
        ...     description="Python for data science and analysis",
        ... )
        >>> lang_context.key
        'python_data_001'
        >>> lang_context.language
        'python'
        >>> lang_context.context
        'data'
    """

    key: str
    language: str
    context: str
    description: str
    embedding: list[float] | None = None


class Preference(BaseModel):
    """A model representing a preference in LanceDB.

    Attributes:
        key (str): Key identifier for the preference.
        name (str): Name of the preferred tool or library.
        description (str): Description of the preference.
        language_context_key (str): Reference to the associated language context.
        priority (int, optional): Priority level (1-10, higher is more important).
        tags (list[str], optional): Tags for categorization.

    Examples:
        >>> preference = Preference(
        ...     key="pref_001",
        ...     name="polars",
        ...     description="Fast DataFrame library for Python",
        ...     language_context_key="python_data_001",
        ...     priority=9,
        ... )
        >>> preference.name
        'polars'
    """

    key: str
    name: str
    description: str
    language_context_key: str
    priority: int
    tags: list[str] | None = None


class Guideline(BaseModel):
    """A model representing a guideline in LanceDB.

    Attributes:
        key (str): Key identifier for the guideline.
        name (str): Name of the guideline.
        description (str): Detailed description of the guideline.
        language_context_key (str): Reference to the associated language context.
        category (str, optional): Category of the guideline.
        examples (list[str], optional): Example implementations.

    Examples:
        >>> guideline = Guideline(
        ...     key="guide_001",
        ...     name="Use type hints",
        ...     description="Always use type hints in Python functions",
        ...     language_context_key="python_data_001",
        ...     category="code_quality",
        ... )
        >>> guideline.name
        'Use type hints'
    """

    key: str
    name: str
    description: str
    language_context_key: str
    category: str | None = None
    examples: list[str] | None = None


class Rule(BaseModel):
    """A model representing a rule in LanceDB.

    Attributes:
        key (str): Key identifier for the rule.
        name (str): Name of the rule.
        description (str): Description of the rule.
        language_context_key (str): Reference to the associated language context.
        enforcement_level (int): Enforcement level (1-10, higher is stricter).
        rule_type (str, optional): Type of rule (e.g., "style", "security").
        violations_action (str, optional): Action to take on violations.

    Examples:
        >>> rule = Rule(
        ...     key="rule_001",
        ...     name="No global variables",
        ...     description="Avoid using global variables",
        ...     language_context_key="python_data_001",
        ...     enforcement_level=8,
        ...     rule_type="best_practice",
        ... )
        >>> rule.name
        'No global variables'
        >>> rule.enforcement_level
        8
    """

    key: str
    name: str
    description: str
    language_context_key: str
    enforcement_level: int
    rule_type: str | None = None
    violations_action: str | None = None


class SourceStructure(BaseModel):
    """A model representing a source structure in LanceDB.

    Attributes:
        key (str): Key identifier for the source structure.
        path (str): File or directory path.
        description (str): Description of the structure.
        language_context_key (str): Reference to the associated language context.
        structure_type (str, optional): Type of structure (e.g., "module", "package").

    Examples:
        >>> src_structure = SourceStructure(
        ...     key="struct_001",
        ...     path="src/data_processing",
        ...     description="Data processing module",
        ...     language_context_key="python_data_001",
        ...     structure_type="module",
        ... )
        >>> src_structure.path
        'src/data_processing'
    """

    key: str
    path: str
    description: str
    language_context_key: str
    structure_type: str | None = None


class Code(BaseModel):
    """A model representing code snippets in LanceDB.

    Attributes:
        key (str): Key identifier for the code.
        name (str): Name or title of the code.
        content (str): The actual code content.
        language_context_key (str): Reference to the associated language context.
        description (str, optional): Description of what the code does.
        tags (list[str], optional): Tags for categorization.
        embedding (list[float], optional): Vector embedding for similarity search.

    Examples:
        >>> code = Code(
        ...     key="code_001",
        ...     name="data_loader",
        ...     content="def load_data(path): ...",
        ...     language_context_key="python_data_001",
        ...     description="Function to load data from file",
        ... )
        >>> code.name
        'data_loader'
        >>> code.content
        'def load_data(path): ...'
    """

    key: str
    name: str
    content: str
    language_context_key: str
    description: str | None = None
    tags: list[str] | None = None
    embedding: list[float] | None = None


class Abstraction(BaseModel):
    """A model representing abstractions in LanceDB.

    Attributes:
        key (str): Key identifier for the abstraction.
        name (str): Name of the abstraction.
        description (str): Description of the abstraction.
        language_context_key (str): Reference to the associated language context.
        abstraction_type (str, optional): Type of abstraction
            (e.g., "pattern", "template").
        content (str, optional): Content or implementation of the abstraction.
        related_code_keys (list[str], optional): Related code snippet IDs.
        embedding (list[float], optional): Vector embedding for similarity search.

    Examples:
        >>> abstraction = Abstraction(
        ...     key="abs_001",
        ...     name="Repository Pattern",
        ...     description="Data access abstraction pattern",
        ...     language_context_key="python_data_001",
        ...     abstraction_type="pattern",
        ... )
        >>> abstraction.abstraction_type
        'pattern'
        >>> abstraction.name
        'Repository Pattern'
    """

    key: str
    name: str
    description: str
    language_context_key: str
    abstraction_type: str | None = None
    content: str | None = None
    related_code_keys: list[str] | None = None
    embedding: list[float] | None = None


class QueryFilter(BaseModel):
    """A model for querying LanceDB tables.

    Attributes:
        table (TableNameEnum): The table to query.
        filter_conditions (dict, optional): Filter conditions for the query.
        limit (int, optional): Maximum number of results.
        offset (int, optional): Number of results to skip.

    Examples:
        >>> query = QueryFilter(
        ...     table=TableNameEnum.PREFERENCE,
        ...     filter_conditions={"language_context_key": "python_data_001"},
        ...     limit=10
        ... )
        >>> query.table
        <TableNameEnum.PREFERENCE: 'preferences'>
        >>> query.filter_conditions
        {'language_context_key': 'python_data_001'}
    """

    table: TableNameEnum
    filter_conditions: dict | None = None
    limit: int | None = None
    offset: int | None = None


SCHEMAS = {
    TableNameEnum.LANG_CONTEXT: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("language", pa.string()),
            pa.field("context", pa.string()),
            pa.field("description", pa.string()),
            pa.field("embedding", pa.list_(pa.float64())),
        ]
    ),
    TableNameEnum.PREFERENCE: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("name", pa.string()),
            pa.field("description", pa.string()),
            pa.field("language_context_key", pa.string()),
            pa.field("priority", pa.int32()),
            pa.field("tags", pa.list_(pa.string())),
        ]
    ),
    TableNameEnum.GUIDELINE: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("name", pa.string()),
            pa.field("description", pa.string()),
            pa.field("language_context_key", pa.string()),
            pa.field("category", pa.string()),
            pa.field("examples", pa.list_(pa.string())),
        ]
    ),
    TableNameEnum.RULE: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("name", pa.string()),
            pa.field("description", pa.string()),
            pa.field("language_context_key", pa.string()),
            pa.field("enforcement_level", pa.int32()),
            pa.field("rule_type", pa.string()),
            pa.field("violations_action", pa.string()),
        ]
    ),
    TableNameEnum.SRC_STRUCTURE: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("path", pa.string()),
            pa.field("description", pa.string()),
            pa.field("language_context_key", pa.string()),
            pa.field("structure_type", pa.string()),
        ]
    ),
    TableNameEnum.CODE: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("name", pa.string()),
            pa.field("content", pa.string()),
            pa.field("language_context_key", pa.string()),
            pa.field("description", pa.string()),
            pa.field("tags", pa.list_(pa.string())),
            pa.field("embedding", pa.list_(pa.float64())),
        ]
    ),
    TableNameEnum.ABSTRACTION: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("name", pa.string()),
            pa.field("description", pa.string()),
            pa.field("language_context_key", pa.string()),
            pa.field("abstraction_type", pa.string()),
            pa.field("content", pa.string()),
            pa.field("related_code_keys", pa.list_(pa.string())),
            pa.field("embedding", pa.list_(pa.float64())),
        ]
    ),
}
