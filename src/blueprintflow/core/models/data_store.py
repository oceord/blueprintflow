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
        embedding (list[float]): Vector embedding for similarity search.

    Examples:
        >>> lang_context = LanguageContext(
        ...     key="python_data_001",
        ...     language="python",
        ...     context="data",
        ...     description="Python for data science and analysis",
        ...     embedding=[1, 1, 1],
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
    embedding: list[float]


class Preference(BaseModel):
    """A model representing a preference in LanceDB.

    Attributes:
        key (str): Key identifier for the preference.
        language_context_key (str): Reference to the associated language context.
        name (str): Name of the preferred tool or library.
        description (str): Description of the preference.
        tags (list[str], optional): Tags for categorization.
        embedding (list[float]): Vector embedding for similarity search.

    Examples:
        >>> preference = Preference(
        ...     key="pref_001",
        ...     language_context_key="python_data_001",
        ...     name="polars",
        ...     description="Fast DataFrame library for Python",
        ...     embedding=[1, 1, 1],
        ... )
        >>> preference.name
        'polars'
    """

    key: str
    language_context_key: str
    name: str
    description: str
    tags: list[str] | None = None
    embedding: list[float]


class Rule(BaseModel):
    """A model representing a rule in LanceDB.

    Attributes:
        key (str): Key identifier for the rule.
        language_context_key (str): Reference to the associated language context.
        name (str): Name of the rule.
        description (str): Description of the rule.
        rule_type (str, optional): Type of rule (e.g., "style", "security").
        violations_action (str, optional): Action to take on violations.
        embedding (list[float]): Vector embedding for similarity search.

    Examples:
        >>> rule = Rule(
        ...     key="rule_001",
        ...     language_context_key="python_data_001",
        ...     name="No global variables",
        ...     description="Avoid using global variables",
        ...     rule_type="best_practice",
        ...     embedding=[1, 1, 1],
        ... )
        >>> rule.name
        'No global variables'
    """

    key: str
    language_context_key: str
    name: str
    description: str
    rule_type: str | None = None
    violations_action: str | None = None
    embedding: list[float]


class Guideline(BaseModel):
    """A model representing a guideline in LanceDB.

    Attributes:
        key (str): Key identifier for the guideline.
        language_context_key (str): Reference to the associated language context.
        name (str): Name of the guideline.
        description (str): Detailed description of the guideline.
        category (str, optional): Category of the guideline.
        examples (list[str], optional): Example implementations.
        embedding (list[float]): Vector embedding for similarity search.

    Examples:
        >>> guideline = Guideline(
        ...     key="guide_001",
        ...     language_context_key="python_data_001",
        ...     name="Use type hints",
        ...     description="Always use type hints in Python functions",
        ...     category="code_quality",
        ...     embedding=[1, 1, 1],
        ... )
        >>> guideline.name
        'Use type hints'
    """

    key: str
    language_context_key: str
    name: str
    description: str
    category: str | None = None
    examples: list[str] | None = None
    embedding: list[float]


class SourceStructure(BaseModel):
    """A model representing a source structure in LanceDB.

    Attributes:
        key (str): Key identifier for the source structure.
        language_context_key (str): Reference to the associated language context.
        path (str): File or directory path.
        description (str): Description of the structure.
        structure_type (str, optional): Type of structure (e.g., "module", "package").
        embedding (list[float]): Vector embedding for similarity search.

    Examples:
        >>> src_structure = SourceStructure(
        ...     key="struct_001",
        ...     language_context_key="python_data_001",
        ...     path="src/data_processing",
        ...     description="Data processing module",
        ...     structure_type="file",
        ...     embedding=[1, 1, 1],
        ... )
        >>> src_structure.path
        'src/data_processing'
    """

    key: str
    language_context_key: str
    path: str
    description: str
    structure_type: str | None = None
    embedding: list[float]


class Abstraction(BaseModel):
    """A model representing abstractions in LanceDB.

    Attributes:
        key (str): Key identifier for the abstraction.
        language_context_key (str): Reference to the associated language context.
        name (str): Name of the abstraction.
        description (str): Description of the abstraction.
        abstraction_type (str, optional): Type of abstraction
            (e.g., "pattern", "template").
        content (str, optional): Content or implementation of the abstraction.
        tags (list[str], optional): Tags for categorization.
        embedding (list[float]): Vector embedding for similarity search.

    Examples:
        >>> abstraction = Abstraction(
        ...     key="abs_001",
        ...     language_context_key="python_data_001",
        ...     name="Repository Pattern",
        ...     description="Data access abstraction pattern",
        ...     abstraction_type="pattern",
        ...     embedding=[1, 1, 1],
        ... )
        >>> abstraction.abstraction_type
        'pattern'
        >>> abstraction.name
        'Repository Pattern'
    """

    key: str
    language_context_key: str
    name: str
    description: str
    abstraction_type: str | None = None
    content: str | None = None
    tags: list[str] | None = None
    embedding: list[float]


class Code(BaseModel):
    """A model representing code snippets in LanceDB.

    Attributes:
        key (str): Key identifier for the code.
        language_context_key (str): Reference to the associated language context.
        name (str): Name or title of the code.
        description (str, optional): Description of what the code does.
        content (str): The actual code content.
        tags (list[str], optional): Tags for categorization.
        embedding (list[float]): Vector embedding for similarity search.

    Examples:
        >>> code = Code(
        ...     key="code_001",
        ...     language_context_key="python_data_001",
        ...     name="data_loader",
        ...     description="Function to load data from file",
        ...     content="def load_data(path): ...",
        ...     embedding=[0.5, 0.5, 0.5],
        ... )
        >>> code.name
        'data_loader'
        >>> code.content
        'def load_data(path): ...'
    """

    key: str
    language_context_key: str
    name: str
    description: str
    content: str
    tags: list[str] | None = None
    embedding: list[float]


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
            pa.field("language_context_key", pa.string()),
            pa.field("name", pa.string()),
            pa.field("description", pa.string()),
            pa.field("tags", pa.list_(pa.string())),
            pa.field("embedding", pa.list_(pa.float64())),
        ]
    ),
    TableNameEnum.GUIDELINE: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("language_context_key", pa.string()),
            pa.field("name", pa.string()),
            pa.field("description", pa.string()),
            pa.field("category", pa.string()),
            pa.field("examples", pa.list_(pa.string())),
            pa.field("embedding", pa.list_(pa.float64())),
        ]
    ),
    TableNameEnum.RULE: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("language_context_key", pa.string()),
            pa.field("name", pa.string()),
            pa.field("description", pa.string()),
            pa.field("rule_type", pa.string()),
            pa.field("violations_action", pa.string()),
            pa.field("embedding", pa.list_(pa.float64())),
        ]
    ),
    TableNameEnum.SRC_STRUCTURE: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("language_context_key", pa.string()),
            pa.field("path", pa.string()),
            pa.field("description", pa.string()),
            pa.field("structure_type", pa.string()),
            pa.field("embedding", pa.list_(pa.float64())),
        ]
    ),
    TableNameEnum.CODE: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("language_context_key", pa.string()),
            pa.field("name", pa.string()),
            pa.field("description", pa.string()),
            pa.field("content", pa.string()),
            pa.field("tags", pa.list_(pa.string())),
            pa.field("embedding", pa.list_(pa.float64())),
        ]
    ),
    TableNameEnum.ABSTRACTION: pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("language_context_key", pa.string()),
            pa.field("name", pa.string()),
            pa.field("description", pa.string()),
            pa.field("abstraction_type", pa.string()),
            pa.field("content", pa.string()),
            pa.field("tags", pa.list_(pa.string())),
            pa.field("embedding", pa.list_(pa.float64())),
        ]
    ),
}
