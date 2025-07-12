from blueprintflow.core.models.store import KuzuTableProperty


def gen_cs_table_properties(properties: list[KuzuTableProperty]) -> str:
    """Generate a comma-separated string of properties for a Kuzu table.

    This function takes a list of KuzuProperty objects and generates a string
    representation of the properties, including their names, types, and default values.

    Args:
        properties (list[KuzuProperty]): A list of KuzuProperty objects.

    Returns:
        str: A comma-separated string of properties in the format
            "<name> <type> DEFAULT <default>".

    Examples:
        >>> props = [
        ...     KuzuProperty("id", "SERIAL"),
        ...     KuzuProperty("name", "STRING", "default_name"),
        ... ]
        >>> gen_cs_properties(props)
        'id SERIAL, name STRING DEFAULT default_name'
    """
    return ", ".join(
        f"{prop.name} {prop.type}{f' DEFAULT {prop.default}' if prop.default else ''}"
        for prop in properties
    )
