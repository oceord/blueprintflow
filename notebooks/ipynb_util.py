from pprint import pprint

LIST_SLICE_THRESHOLD = 3
STR_SLICE_THRESHOLD = 250
STR_SLICE_PLACEHOLDER = " [...]"


def pprint_lancedb_record(  # noqa: PLR0913
    record: dict,
    *,
    fields_to_ignore: list[str] | None = None,
    fields_to_clip_at_first_line: list[str] | None = None,
    compact: bool = True,
    sort_dicts: bool = False,
    underscore_numbers: bool = True,
) -> None:
    for field in fields_to_ignore or []:
        record.pop(field)
    for newline_replace_field in fields_to_clip_at_first_line or []:
        first_newline_pos = record[newline_replace_field].find("\n")
        record[newline_replace_field] = (
            record[newline_replace_field][:first_newline_pos] + " [...]"
        ).replace("  ", " ")
    record_str_items = {
        k: (
            v[: STR_SLICE_THRESHOLD - len(STR_SLICE_PLACEHOLDER)]
            + STR_SLICE_PLACEHOLDER
        ).replace("  ", " ")
        for k, v in record.items()
        if isinstance(v, str) and len(v) > STR_SLICE_THRESHOLD
    }
    record_list_items = {
        k: v[:LIST_SLICE_THRESHOLD]
        for k, v in record.items()
        if isinstance(v, list) and len(v) > LIST_SLICE_THRESHOLD
    }
    pprint(
        {**record, **record_str_items, **record_list_items},
        compact=compact,
        sort_dicts=sort_dicts,
        underscore_numbers=underscore_numbers,
    )
