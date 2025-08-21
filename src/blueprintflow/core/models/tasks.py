from enum import StrEnum

from pydantic import BaseModel

from blueprintflow.core.models.data_store import (
    Abstraction,
    Code,
    Guideline,
    LanguageContext,
    Preference,
    Rule,
    SourceStructure,
)


class TaskStatusEnum(StrEnum):
    """Enumeration of task statuses.

    This enum defines the various statuses that a task can have, indicating
    whether it was successful, failed, or is in progress.

    Members:
        CANCELLED: The task was cancelled before completion.
        FAILURE: The task failed to complete.
        IN_PROGRESS: The task is currently in progress.
        PENDING: The task is pending and has not started yet.
        SKIPPED: The task was skipped.
        SUCCESS: The task completed successfully.
        TIMED_OUT: The task timed out before completion.
        UNKNOWN: The status of the task is unknown.
    """

    CANCELLED = "cancelled"
    FAILURE = "failure"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    SKIPPED = "skipped"
    SUCCESS = "success"
    TIMED_OUT = "timed_out"
    UNKNOWN = "unknown"


class CreateLanguageContextTask(BaseModel):
    """A task for creating a language context record in the database.

    Attributes:
        key (str, optional): Key identifier for the language context.
        language (str): The programming language (e.g., "python", "javascript").
        context (str): The context or domain (e.g., "data", "web", "ml").
        description (str): A detailed description of the language context.
        embedding (list[float], optional): Vector embedding for similarity search.
    """

    key: str | None = None
    language: str
    context: str
    description: str
    embedding: list[float] | None = None

    def as_text_features(self) -> str:
        """Extracts a string of key features for creating a vector embedding.

        The method ensures that the most semantically relevant information is
        included in a format that a text-embedding model can process effectively.

        Returns:
            str: A formatted string containing the language context's key text features.
        """
        return (
            f"Language: {self.language}; "
            f"Context: {self.context}; "
            f"Description: {self.description}"
        )

    def to_data_store_model(self) -> LanguageContext:
        """Converts the current task instance into a LanguageContext model instance.

        This method unpacks the dictionary representation of the current task
        (obtained via model_dump()) into the LanguageContext constructor.

        Returns:
            LanguageContext: An instance of LanguageContext populated with the data
                from this task instance.
        """
        return LanguageContext(**self.model_dump())


class CreatePreferenceTask(BaseModel):
    """A task for creating a preference record.

    Attributes:
        key (str, optional): Key identifier for the preference.
        language_context_key (str): Reference to the associated language context.
        name (str): Name of the preferred tool or library.
        description (str): Description of the preference.
        tags (list[str], optional): Tags for categorization.
        embedding (list[float], optional): Vector embedding for similarity search.
    """

    key: str | None = None
    language_context_key: str
    name: str
    description: str
    tags: list[str] | None = None
    embedding: list[float] | None = None

    def as_text_features(self) -> str:
        """Extracts a string of key features for creating a vector embedding.

        The method ensures that the most semantically relevant information is
        included in a format that a text-embedding model can process effectively.

        Returns:
            str: A formatted string containing the preference's key text features.
        """
        str_tags = "; Tags: " + ", ".join(self.tags) if self.tags is not None else ""
        return f"Name: {self.name}; Description: {self.description}{str_tags}"

    def to_data_store_model(self) -> Preference:
        """Converts the current task instance into a Preference model instance.

        This method unpacks the dictionary representation of the current task
        (obtained via model_dump()) into the Preference constructor.

        Returns:
            Preference: An instance of Preference populated with the data
                from this task instance.
        """
        return Preference(**self.model_dump())


class CreateRuleTask(BaseModel):
    """A task for creating a rule record.

    Attributes:
        key (str, optional): Key identifier for the rule.
        language_context_key (str): Reference to the associated language context.
        name (str): Name of the rule.
        description (str): Description of the rule.
        rule_type (str, optional): Type of rule (e.g., "style", "security").
        violations_action (str, optional): Action to take on violations.
        embedding (list[float], optional): Vector embedding for similarity search.
    """

    key: str | None = None
    language_context_key: str
    name: str
    description: str
    rule_type: str | None = None
    violations_action: str | None = None
    embedding: list[float] | None = None

    def as_text_features(self) -> str:
        """Extracts a string of key features for creating a vector embedding.

        The method ensures that the most semantically relevant information is
        included in a format that a text-embedding model can process effectively.

        Returns:
            str: A formatted string containing the rule's key text features.
        """
        return (
            f"Name: {self.name}; "
            f"Description: {self.description}; "
            f"Type: {self.rule_type}"
        )

    def to_data_store_model(self) -> Rule:
        """Converts the current task instance into a Rule model instance.

        This method unpacks the dictionary representation of the current task
        (obtained via model_dump()) into the Rule constructor.

        Returns:
            Rule: An instance of Rule populated with the data
                from this task instance.
        """
        return Rule(**self.model_dump())


class CreateGuidelineTask(BaseModel):
    """A task for creating a guideline record.

    Attributes:
        key (str, optional): Key identifier for the guideline.
        language_context_key (str): Reference to the associated language context.
        name (str): Name of the guideline.
        description (str): Detailed description of the guideline.
        category (str, optional): Category of the guideline.
        examples (list[str], optional): Example implementations.
        embedding (list[float], optional): Vector embedding for similarity search.
    """

    key: str | None = None
    language_context_key: str
    name: str
    description: str
    category: str | None = None
    examples: list[str] | None = None
    embedding: list[float] | None = None

    def as_text_features(self) -> str:
        """Extracts a string of key features for creating a vector embedding.

        The method ensures that the most semantically relevant information is
        included in a format that a text-embedding model can process effectively.

        Returns:
            str: A formatted string containing the guideline's key text features.
        """
        return (
            f"Name: {self.name}; "
            f"Description: {self.description}; "
            f"Category: {self.category}"
        )

    def to_data_store_model(self) -> Guideline:
        """Converts the current task instance into a Guideline model instance.

        This method unpacks the dictionary representation of the current task
        (obtained via model_dump()) into the Guideline constructor.

        Returns:
            Guideline: An instance of Guideline populated with the data
                from this task instance.
        """
        return Guideline(**self.model_dump())


class CreateSrcStructureTask(BaseModel):
    """A task for creating a src structure record.

    Attributes:
        key (str, optional): Key identifier for the source structure.
        language_context_key (str): Reference to the associated language context.
        path (str): File or directory path.
        description (str): Description of the structure.
        structure_type (str, optional): Type of structure (e.g., "directory", "file").
        embedding (list[float], optional): Vector embedding for similarity search.
    """

    key: str | None = None
    language_context_key: str
    path: str
    description: str
    structure_type: str | None = None
    embedding: list[float] | None = None

    def as_text_features(self) -> str:
        """Extracts a string of key features for creating a vector embedding.

        The method ensures that the most semantically relevant information is
        included in a format that a text-embedding model can process effectively.

        Returns:
            str: A formatted string containing the source structure's key text features.
        """
        return (
            f"Path: {self.path}; "
            f"Description: {self.description}"
            f"Type: {self.structure_type}; "
        )

    def to_data_store_model(self) -> SourceStructure:
        """Converts the current task instance into a SourceStructure model instance.

        This method unpacks the dictionary representation of the current task
        (obtained via model_dump()) into the SourceStructure constructor.

        Returns:
            SourceStructure: An instance of SourceStructure populated with the data
                from this task instance.
        """
        return SourceStructure(**self.model_dump())


class CreateAstractionTask(BaseModel):
    """A task for creating an abstraction record.

    Attributes:
        key (str, optional): Key identifier for the abstraction.
        language_context_key (str): Reference to the associated language context.
        name (str): Name of the abstraction.
        description (str): Description of the abstraction.
        abstraction_type (str, optional): Type of abstraction
            (e.g., "pattern", "template").
        content (str, optional): Content or implementation of the abstraction.
        tags (list[str], optional): Tags for categorization.
        embedding (list[float], optional): Vector embedding for similarity search.
    """

    key: str | None = None
    language_context_key: str
    name: str
    description: str
    abstraction_type: str | None = None
    content: str | None = None
    tags: list[str] | None = None
    embedding: list[float] | None = None

    def as_text_features(self) -> str:
        """Extracts a string of key features for creating a vector embedding.

        The method ensures that the most semantically relevant information is
        included in a format that a text-embedding model can process effectively.

        Returns:
            str: A formatted string containing the abstraction's key text features.
        """
        str_tags = (
            "; Tags: " + ", ".join(self.tags) + ";" if self.tags is not None else ""
        )
        return (
            f"Name: {self.name}; "
            f"Description: {self.description}; "
            f"Type: {self.abstraction_type}"
            f"{str_tags}"
            f"Content:\n{self.content}"
        )

    def to_data_store_model(self) -> Abstraction:
        """Converts the current task instance into an Abstraction model instance.

        This method unpacks the dictionary representation of the current task
        (obtained via model_dump()) into the Abstraction constructor.

        Returns:
            Abstraction: An instance of Abstraction populated with the data
                from this task instance.
        """
        return Abstraction(**self.model_dump())


class CreateCodeTask(BaseModel):
    """A task for creating a code record.

    Attributes:
        key (str, optional): Key identifier for the code.
        language_context_key (str): Reference to the associated language context.
        name (str): Name or title of the code.
        description (str, optional): Description of what the code does.
        content (str): The actual code content.
        tags (list[str], optional): Tags for categorization.
        embedding (list[float], optional): Vector embedding for similarity search.
    """

    key: str | None = None
    language_context_key: str
    name: str
    description: str
    content: str
    tags: list[str] | None = None
    embedding: list[float] | None = None

    def as_text_features(self) -> str:
        """Extracts a string of key features for creating a vector embedding.

        The method ensures that the most semantically relevant information is
        included in a format that a text-embedding model can process effectively.

        Returns:
            str: A formatted string containing the code's key text features.
        """
        str_tags = (
            "; Tags: " + ", ".join(self.tags) + ";" if self.tags is not None else ""
        )
        return (
            f"Name: {self.name}; "
            f"Description: {self.description}; "
            f"{str_tags}"
            f"Content:\n{self.content}"
        )

    def to_data_store_model(self) -> Code:
        """Converts the current task instance into a Code model instance.

        This method unpacks the dictionary representation of the current task
        (obtained via model_dump()) into the Code constructor.

        Returns:
            Code: An instance of Code populated with the data
                from this task instance.
        """
        return Code(**self.model_dump())
