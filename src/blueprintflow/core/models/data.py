from enum import Enum


class EmbeddedDataEnum(str, Enum):
    """Enumeration of supported embedded data items.

    This enum defines the names of the embedded data items supported by BlueprintFlow.
    Each member of the enum represents a specific embedded data item.
    """

    lancedb = "lancedb"
    kuzu = "kuzudb"
