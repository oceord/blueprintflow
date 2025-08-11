from blueprintflow.core.models.tasks import (
    CreateAstractionTask,
    CreateCodeTask,
    CreateGuidelineTask,
    CreateLanguageContextTask,
    CreatePreferenceTask,
    CreateRuleTask,
    CreateSrcStructureTask,
    TaskStatusEnum,
)
from blueprintflow.helpers.xdg.data import UserData
from blueprintflow.store.handlers.kuzu_handler import Kuzu


class StoreManager:
    """High-level component that manages database interactions for BlueprintFlow.

    This class facilitates the creation and management of entities and their
    relationships that are essencial for BlueprintFlow to function properly.

    Attributes:
        kuzu_handler (Kuzu): An instance of the Kuzu handler used to interact with the
            Kuzu database.
        lance_handler (LanceDB): An instance of the LanceDB handler used to interact
            with the LanceDB database.

    Methods:
        create_lang_context(lang_context_task: CreateLanguageContextTask)
            -> TaskStatusEnum:
            Creates a language context node in the Kuzu database.

        create_preference(preference_task: CreatePreferenceTask) -> TaskStatusEnum:
            Creates a preference node and its relationship to a language context.

        create_guideline(guideline_task: CreateGuidelineTask) -> TaskStatusEnum:
            Creates a guideline node and its relationship to a language context.

        create_rule(rule_task: CreateRuleTask) -> TaskStatusEnum:
            Creates a rule node and its relationship to a language context.

        create_src_structure(src_structure_task: CreateSrcStructureTask)
            -> TaskStatusEnum:
            Creates a source structure node and its relationship to a language context.

        create_code(code_task: CreateCodeTask) -> TaskStatusEnum:
            Placeholder for creating code in LanceDB (not yet implemented).

        create_abstraction(abstraction_task: CreateAstractionTask) -> TaskStatusEnum:
            Placeholder for creating abstraction in LanceDB (not yet implemented).
    """

    def __init__(self, user_data: UserData) -> None:
        """Initialize the StoreManager.

        Args:
            user_data (UserData): User data containing necessary information for
                initializing the Kuzu and LanceDB handlers.
        """
        self.kuzu_handler = Kuzu(user_data)

    def create_lang_context(
        self, lang_context_task: CreateLanguageContextTask
    ) -> TaskStatusEnum:
        """Create a language context node.

        Args:
            lang_context_task (CreateLanguageContextTask): A task containing the
                language context node to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.
        """
        if not self.kuzu_handler.create_node(lang_context_task.language_context):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS

    def create_preference(
        self, preference_task: CreatePreferenceTask
    ) -> TaskStatusEnum:
        """Create a preference node and its relationship to a language context.

        Args:
            preference_task (CreatePreferenceTask): A task containing the preference
                node and its relationship to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.
        """
        if not self.kuzu_handler.create_node(preference_task.preference):
            return TaskStatusEnum.FAILURE
        if not self.kuzu_handler.create_relationship(
            preference_task.language_context_rel
        ):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS

    def create_guideline(self, guideline_task: CreateGuidelineTask) -> TaskStatusEnum:
        """Create a guideline node and its relationship to a language context.

        Args:
            guideline_task (CreateGuidelineTask): A task containing the guideline node
                and its relationship to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.
        """
        if not self.kuzu_handler.create_node(guideline_task.guideline):
            return TaskStatusEnum.FAILURE
        if not self.kuzu_handler.create_relationship(
            guideline_task.language_context_rel
        ):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS

    def create_rule(self, rule_task: CreateRuleTask) -> TaskStatusEnum:
        """Create a rule node and its relationship to a language context.

        Args:
            rule_task (CreateRuleTask): A task containing the rule node and its
                relationship to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.
        """
        if not self.kuzu_handler.create_node(rule_task.rule):
            return TaskStatusEnum.FAILURE
        if not self.kuzu_handler.create_relationship(rule_task.language_context_rel):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS

    def create_src_structure(
        self, src_structure_task: CreateSrcStructureTask
    ) -> TaskStatusEnum:
        """Create a source structure node and its relationship to a language context.

        Args:
            src_structure_task (CreateSrcStructureTask): A task containing the source
                structure node and its relationship to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.
        """
        if not self.kuzu_handler.create_node(src_structure_task.src_structure):
            return TaskStatusEnum.FAILURE
        if not self.kuzu_handler.create_relationship(
            src_structure_task.language_context_rel
        ):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS
