from collections.abc import Iterable
from itertools import chain

from blueprintflow.core.models.store import (
    KuzuMatchCondition,
    KuzuProperty,
    KuzuTableProperty,
)


def gen_cs_table_properties(properties: list[KuzuTableProperty]) -> str:
    """Generate a comma-separated string of properties for a Kuzu table.

    This function takes a list of KuzuTableProperty objects and generates a string
    representation of the properties, including their names, types, and default values.

    Args:
        properties (list[KuzuTableProperty]): A list of KuzuTableProperty objects.

    Returns:
        str: A comma-separated string of properties in the format
            "<name> <type> DEFAULT <default>".

    Examples:
        >>> props = [
        ...     KuzuTableProperty("id", "SERIAL"),
        ...     KuzuTableProperty("name", "STRING", "default_name"),
        ... ]
        >>> gen_cs_table_properties(props)
        'id SERIAL, name STRING DEFAULT default_name'
    """

    def format_default_property(default_prop: str | None) -> str:
        return f" DEFAULT {default_prop}" if default_prop else ""

    return ", ".join(
        f"{prop.name} {prop.type}{format_default_property(prop.default)}"
        for prop in properties
    )


def gen_cs_real_properties(
    properties: list[KuzuProperty] | None, *, curlies: bool = False
) -> str:
    """Generate a comma-separated string of properties with their names and values.

    This function takes a list of KuzuProperty objects and generates a string
    representation of the properties, including their names and values.

    Args:
        properties (list[KuzuProperty] | None): A list of KuzuProperty objects, each
            expected to have a 'name' and 'value' attribute.
        curlies (bool, optional): If True, wraps the result in curly braces.
            Defaults to False.

    Returns:
        str: A string representation of the properties in the format
            "name1: 'value1', name2: 'value2'", optionally wrapped in curly braces if
            curlies is True. Returns an empty string if properties is None.

    Examples:
        >>> props = [
        ...     KuzuProperty("id", "value1"),
        ...     KuzuProperty("name", "value2"),
        ... ]
        >>> gen_cs_real_properties(props)
        "id: 'value1', name: 'value2'"
        >>> gen_cs_real_properties(props, curlies=True)
        "{id: 'value1', name: 'value2'}"
    """
    if properties is None:
        return ""
    buffer = ", ".join(f"{prop.name}: '{prop.value}'" for prop in properties)
    if curlies:
        buffer = f"{{{buffer}}}"
    return buffer


def gen_match_condition(
    from_alias: str,
    to_alias: str,
    from_conditions: list[KuzuMatchCondition],
    to_conditions: list[KuzuMatchCondition],
) -> str:
    """Generate a string of match conditions for a Cypher query.

    This function takes lists of match conditions for source and target nodes and
    generates a string representation of these conditions, joined by AND operators.

    Args:
        from_alias (str): The alias for the source node.
        to_alias (str): The alias for the target node.
        from_conditions (list[KuzuMatchCondition]): A list of match conditions for the
            source node.
        to_conditions (list[KuzuMatchCondition]): A list of match conditions for the
            target node.

    Returns:
        str: A string representation of the match conditions in the format
            "alias1.property1 operation1 'value1'
            AND alias2.property2 operation2 'value2'".

    Examples:
        >>> from_conditions = [
        ...     KuzuMatchCondition(
        ...         property="name",
        ...         operation="=",
        ...         value="waldo"
        ...     )
        ... ]
        >>> to_conditions = [
        ...     KuzuMatchCondition(
        ...         property="name",
        ...         operation="=",
        ...         value="nowhere"
        ...     )
        ... ]
        >>> gen_match_condition("celebrity", "location", from_conditions, to_conditions)
        "celebrity.name = 'waldo' AND location.name = 'nowhere'"
    """

    def _gen_aliased_conditions(
        alias: str, conditions: list[KuzuMatchCondition]
    ) -> Iterable[str]:
        return (
            f"{alias}.{cond.property} {cond.operation} '{cond.value}'"
            for cond in conditions
        )

    return " AND ".join(
        chain(
            _gen_aliased_conditions(from_alias, from_conditions),
            _gen_aliased_conditions(to_alias, to_conditions),
        )
    )
