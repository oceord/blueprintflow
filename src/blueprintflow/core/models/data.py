from enum import Enum


class DataStoreEnum(str, Enum):
    """Enumeration of supported data stores.

    This enum defines the names of the data stores used by BlueprintFlow.
    Each member of the enum represents a specific store.
    """

    LANCEDB = "lancedb"
    KUZU = "kuzudb"
