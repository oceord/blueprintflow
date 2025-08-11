from enum import StrEnum

from pydantic import BaseModel

from blueprintflow.core.models.store import KuzuNode, KuzuRel


class TaskStatusEnum(StrEnum):
    """Enumeration of task statuses.

    This enum defines the various statuses that a task can have, indicating
    whether it was successful, failed, or is in progress.

    Members:
        SUCCESS: The task completed successfully.
        FAILURE: The task failed to complete.
        IN_PROGRESS: The task is currently in progress.
        PENDING: The task is pending and has not started yet.
        CANCELLED: The task was cancelled before completion.
        TIMED_OUT: The task timed out before completion.
        UNKNOWN: The status of the task is unknown.
    """

    SUCCESS = "success"
    FAILURE = "failure"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"
    UNKNOWN = "unknown"


class CreateLanguageContextTask(BaseModel):
    """A task for creating a language context node in the database.

    Attributes:
        language_context (KuzuNode): The language context node to be created.
    """

    language_context: KuzuNode


class CreatePreferenceTask(BaseModel):
    """A task for creating a preference node.

    Attributes:
        preference (KuzuNode): The preference node to be created.
        language_context_rel (KuzuRel): The relationship between the preference and a
            language context.
    """

    preference: KuzuNode
    language_context_rel: KuzuRel


class CreateGuidelineTask(BaseModel):
    """A task for creating a guideline node.

    Attributes:
        guideline (KuzuNode): The guideline node to be created.
        language_context_rel (KuzuRel): The relationship between the guideline and a
            language context.
    """

    guideline: KuzuNode
    language_context_rel: KuzuRel


class CreateRuleTask(BaseModel):
    """A task for creating a rule node.

    Attributes:
        rule (KuzuNode): The rule node to be created.
        language_context_rel (KuzuRel): The relationship between the rule and a language
            context.
    """

    rule: KuzuNode
    language_context_rel: KuzuRel


class CreateSrcStructureTask(BaseModel):
    """A task for creating a src structure node.

    Attributes:
        src_structure (KuzuNode): The source structure node to be created.
        language_context_rel (KuzuRel): The relationship between the source structure
            and a language context.
    """

    src_structure: KuzuNode
    language_context_rel: KuzuRel
