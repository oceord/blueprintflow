from string import Template

CYPHER_GET_TABLES = "CALL SHOW_TABLES() RETURN *"

# DDL templates
TMPL_CYPHER_CREATE_NODE_TABLE = Template(
    "CREATE NODE TABLE IF NOT EXISTS "
    "$name ($cs_properties, PRIMARY KEY ($cs_primary_key));"
)
TMPL_CYPHER_CREATE_REL_TABLE = Template(
    "CREATE REL TABLE IF NOT EXISTS "
    "$name (FROM $from_node_table TO $to_node_table, $cs_properties);"
)

# DML templates
TMPL_CYPHER_CREATE_NODE = Template(
    "CREATE ($table_alias:$table_name {$cs_properties});"
)
TMPL_CYPHER_CREATE_RELATIONSHIP = Template(
    "MATCH ($from_alias:$from_node_table), ($to_alias:$to_node_table) "
    "WHERE $match_condition "
    "CREATE ($from_alias)-[:$rel$rel_properties]->($to_alias);"
)
