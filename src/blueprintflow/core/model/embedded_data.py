from enum import Enum


class EmbeddedDataEnum(str, Enum):
    """Enumeration of supported embedded databases.

    This enum defines the names of the embedded databases supported by BlueprintFlow.
    Each member of the enum represents a specific embedded database.
    """

    lancedb = "lancedb"
    kuzu = "kuzudb"
