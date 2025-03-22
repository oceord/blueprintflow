from blueprintflow.core.models.store import KuzuProperty


def gen_cs_properties(properties: list[KuzuProperty]) -> str:
    """Generate a comma-separated string of properties for a Kuzu node or relationship.

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
