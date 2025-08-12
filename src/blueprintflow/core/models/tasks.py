from enum import StrEnum

from pydantic import BaseModel

from blueprintflow.core.models.store import (
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
        language_context (LanguageContext): The language context to be created.
    """

    language_context: LanguageContext


class CreatePreferenceTask(BaseModel):
    """A task for creating a preference record.

    Attributes:
        preference (Preference): The preference to be created.
    """

    preference: Preference


class CreateGuidelineTask(BaseModel):
    """A task for creating a guideline record.

    Attributes:
        guideline (Guideline): The guideline to be created.
    """

    guideline: Guideline


class CreateRuleTask(BaseModel):
    """A task for creating a rule record.

    Attributes:
        rule (Rule): The rule to be created.
    """

    rule: Rule


class CreateSrcStructureTask(BaseModel):
    """A task for creating a src structure record.

    Attributes:
        src_structure (SourceStructure): The source structure to be created.
    """

    src_structure: SourceStructure


class CreateCodeTask(BaseModel):
    """A task for creating a code record.

    Attributes:
        code (Code): The code to be created.
    """

    code: Code


class CreateAstractionTask(BaseModel):
    """A task for creating an abstraction record.

    Attributes:
        abstraction (Abstraction): The abstraction to be created.
    """

    abstraction: Abstraction
