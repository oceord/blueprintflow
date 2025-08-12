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
from blueprintflow.store.lancedb_handler import LanceDB


class StoreManager:
    """High-level component that manages database interactions for BlueprintFlow.

    This class facilitates the creation and management of entities and their
    relationships that are essential for BlueprintFlow to function properly.

    Attributes:
        lance_handler (LanceDB): An instance of the LanceDB handler used to interact
            with the LanceDB database.
    """

    def __init__(self, user_data: UserData) -> None:
        """Initialize the StoreManager.

        Args:
            user_data (UserData): User data containing necessary information for
                initializing the LanceDB handler.

        Example:
            >>> user_data = UserData()
            >>> store_manager = StoreManager(user_data)
        """
        self.lance_handler = LanceDB(user_data)

    def dispatch_task(  # noqa: PLR0911
        self,
        task: CreateLanguageContextTask
        | CreatePreferenceTask
        | CreateGuidelineTask
        | CreateRuleTask
        | CreateSrcStructureTask
        | CreateAstractionTask
        | CreateCodeTask,
    ) -> TaskStatusEnum:
        """Dispatch a task to its corresponding handler based on the task type.

        This function acts as a dispatcher, routing each task to its specific handler
        method based on the task's type. It supports various task types including
        language contexts, preferences, guidelines, rules, source structures,
        abstractions, and code elements.

        Args:
            task: A task object representing the entity to be created. The task must be
                one of the supported types, each containing necessary information for
                creating its specific entity.

        Returns:
            TaskStatusEnum: The status of the task execution, indicating success or
                failure.

        Example:
            >>> from blueprintflow.core.models.tasks import CreateRuleTask
            >>> task = CreateRuleTask(  # doctest: +SKIP
            ...     rule={"name": "rule1", "description": "A sample rule"}
            ... )
            >>> store_manager.dispatch_task(task)  # doctest: +SKIP
        """
        match task:
            case CreateLanguageContextTask() as t:
                return self.create_lang_context(t)
            case CreatePreferenceTask() as t:
                return self.create_preference(t)
            case CreateGuidelineTask() as t:
                return self.create_guideline(t)
            case CreateRuleTask() as t:
                return self.create_rule(t)
            case CreateSrcStructureTask() as t:
                return self.create_src_structure(t)
            case CreateAstractionTask() as t:
                return self.create_abstraction(t)
            case CreateCodeTask() as t:
                return self.create_code(t)

    def create_lang_context(
        self, lang_context_task: CreateLanguageContextTask
    ) -> TaskStatusEnum:
        """Create a language context record.

        Args:
            lang_context_task (CreateLanguageContextTask): A task containing the
                language context record to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.

        Example:
            >>> from blueprintflow.core.models.tasks import CreateLanguageContextTask
            >>> lang_context_task = CreateLanguageContextTask(  # doctest: +SKIP
            ...     language_context={"name": "Python", "version": "3.8"}
            ... )
            >>> store_manager.create_lang_context(lang_context_task)  # doctest: +SKIP
        """
        # TODO: gen embedding if not provided
        if not self.lance_handler.create_record(lang_context_task.language_context):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS

    def create_preference(
        self, preference_task: CreatePreferenceTask
    ) -> TaskStatusEnum:
        """Create a preference record.

        Args:
            preference_task (CreatePreferenceTask): A task containing the preference
                record to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.

        Example:
            >>> from blueprintflow.core.models.tasks import CreatePreferenceTask
            >>> preference_task = CreatePreferenceTask(  # doctest: +SKIP
            ...     preference={"theme": "dark", "font_size": 12}
            ... )
            >>> store_manager.create_preference(preference_task)  # doctest: +SKIP
        """
        if not self.lance_handler.create_record(preference_task.preference):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS

    def create_guideline(self, guideline_task: CreateGuidelineTask) -> TaskStatusEnum:
        """Create a guideline record.

        Args:
            guideline_task (CreateGuidelineTask): A task containing the guideline
                record to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.

        Example:
            >>> from blueprintflow.core.models.tasks import CreateGuidelineTask
            >>> guideline_task = CreateGuidelineTask(  # doctest: +SKIP
            ...     guideline={"name": "coding_standard", "description": "Follow PEP8"}
            ... )
            >>> store_manager.create_guideline(guideline_task)  # doctest: +SKIP
        """
        if not self.lance_handler.create_record(guideline_task.guideline):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS

    def create_rule(self, rule_task: CreateRuleTask) -> TaskStatusEnum:
        """Create a rule record.

        Args:
            rule_task (CreateRuleTask): A task containing the rule record to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.

        Example:
            >>> from blueprintflow.core.models.tasks import CreateRuleTask
            >>> rule_task = CreateRuleTask(  # doctest: +SKIP
            ...     rule={"name": "max_line_length", "value": 79}
            ... )
            >>> store_manager.create_rule(rule_task)  # doctest: +SKIP
        """
        if not self.lance_handler.create_record(rule_task.rule):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS

    def create_src_structure(
        self, src_structure_task: CreateSrcStructureTask
    ) -> TaskStatusEnum:
        """Create a source structure record.

        Args:
            src_structure_task (CreateSrcStructureTask): A task containing the source
                structure record to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.

        Example:
            >>> from blueprintflow.core.models.tasks import CreateSrcStructureTask
            >>> src_structure_task = CreateSrcStructureTask(  # doctest: +SKIP
            ...     src_structure={"project": "my_project", "structure": "/src/main.py"}
            ... )
            >>> store_manager.create_src_structure(src_structure_task)  # doctest: +SKIP
        """
        if not self.lance_handler.create_record(src_structure_task.src_structure):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS

    def create_abstraction(
        self, abstraction_task: CreateAstractionTask
    ) -> TaskStatusEnum:
        """Create an abstraction record.

        Args:
            abstraction_task (CreateAstractionTask): A task containing the abstraction
                record to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.

        Example:
            >>> from blueprintflow.core.models.tasks import CreateAstractionTask
            >>> abstraction_task = CreateAstractionTask(  # doctest: +SKIP
            ...     abstraction={
            ...         "name": "abstract_class",
            ...         "description": "An abstract class example"},
            ... )
            >>> store_manager.create_abstraction(abstraction_task)  # doctest: +SKIP
        """
        # TODO: gen embedding if not provided
        if not self.lance_handler.create_record(abstraction_task.abstraction):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS

    def create_code(self, code_task: CreateCodeTask) -> TaskStatusEnum:
        """Create a code record.

        Args:
            code_task (CreateCodeTask): A task containing the code record to be created.

        Returns:
            TaskStatusEnum: The status of the task execution, either SUCCESS or FAILURE.

        Example:
            >>> from blueprintflow.core.models.tasks import CreateCodeTask
            >>> code_task = CreateCodeTask(  # doctest: +SKIP
            ...     code={"function": "def hello_world(): ...", "language": "python"}
            ... )
            >>> store_manager.create_code(code_task)  # doctest: +SKIP
        """
        # TODO: gen embedding if not provided
        if not self.lance_handler.create_record(code_task.code):
            return TaskStatusEnum.FAILURE
        return TaskStatusEnum.SUCCESS
