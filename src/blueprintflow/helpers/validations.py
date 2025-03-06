def eq_struct(src_dict: dict, tgt_dict: dict) -> bool:
    """Compare the structural compatibility of two dictionaries.

    Args:
        src_dict (dict): Source dictionary to compare with
        tgt_dict (dict): Target dictionary to compare to

    Returns:
        bool: True if both dictionaries have identical structure (same keys and types),
              False otherwise

    Examples:
        >>> eq_struct({}, {})
        True

        >>> eq_struct({'a': 1}, {'a': 2})
        True

        >>> eq_struct({'a': 1, 'b': 'foo'}, {'a': 2, 'b': 'bar'})
        True

        >>> eq_struct({'a': 1}, {})
        False

        >>> eq_struct({'a': 1}, {'b': 1})
        False

        >>> eq_struct({'a': 1}, {'a': 1, 'b': 1})
        False

        >>> eq_struct({'a': [1]}, {'a': [2]})
        True

        >>> eq_struct({'a': [1]}, {'a': ['foo', 'waldo']})
        True

        >>> eq_struct({'a': {'b': 1}}, {'a': {'b': 2}})
        True
    """

    def get_types(d: dict) -> dict:
        result: dict = {}
        for k, v in d.items():
            match v:
                case dict():
                    result[k] = get_types(v)
                case _:
                    result[k] = type(v).__name__
        return result

    return get_types(src_dict) == get_types(tgt_dict)
