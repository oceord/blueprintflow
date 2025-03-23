from string import Template

CYPHER_GET_TABLES = "CALL SHOW_TABLES() RETURN *"

# DDL templates
TMPL_CYPHER_CREATE_NODE_TABLE = Template(
    "CREATE NODE TABLE IF NOT EXISTS "
    "$name ($cs_properties, PRIMARY KEY ($cs_primary_key))"
)
TMPL_CYPHER_CREATE_REL_TABLE = Template(
    "CREATE REL TABLE IF NOT EXISTS $name (FROM $from_node TO $to_node, $cs_properties)"
)
