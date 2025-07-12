from pathlib import Path

from blueprintflow.core.models.store import DataStoreEnum
from blueprintflow.helpers.xdg.constants import (
    BPF_LOG_FILE_NAME,
    BPF_USER_DATA_DIR_NAME,
    LINUX_USER_DATA_DIR,
    MACOS_USER_DATA_DIR,
    SYSTEM,
    WINDOWS_USER_DATA_DIR,
)


def get_platform_user_data_dir() -> Path:
    """Retrieve the user data directory for the current platform.

    This function determines the appropriate user data directory for the
    current operating system. If the operating system is not supported, a
    ValueError is raised.

    Raises:
        ValueError: If the operating system is not supported.

    Returns:
        Path: The path to the system data directory.
    """
    match SYSTEM:
        case "Linux":
            data_dir = LINUX_USER_DATA_DIR
        case "Darwin":
            data_dir = MACOS_USER_DATA_DIR
        case "Windows":
            data_dir = WINDOWS_USER_DATA_DIR
        case _:
            msg = f"Unsupported operating system: {SYSTEM}"
            raise ValueError(msg)
    return data_dir


def init_user_data_dir(data_dir: Path) -> None:
    """Initialize the user data directory.

    This function ensures that the user data directory exists by creating it
    if it does not already exist.

    Args:
        data_dir (Path): The path to the user data directory.
    """
    data_dir.mkdir(parents=True, exist_ok=True)


class UserData:
    """Manages user data directories and files.

    This class handles the initialization and management of user data directories
    and files, including the log file and embedded data files. It ensures that
    the necessary directories and files are created and accessible.

    Attributes:
        _user_data_dir (Path): The path to the user data directory.
        log_file (Path): The path to the log file within the user data directory.
        lancedb_path (Path): The path to the LanceDB file within the user data
            directory.
        kuzu_path (Path): The path to the Kuzu directory within the user data directory.
    """

    def __init__(self, user_data_dir: Path | None = None) -> None:
        """Initialize the UserData instance.

        This constructor initializes the user data directory and ensures that
        the necessary files and subdirectories are created. If a user data directory
        is not provided, it defaults to the platform-specific user data directory.

        Args:
            user_data_dir (Path, optional): The path to the user data directory.
                If not provided, the default platform-specific user data directory is
                used. Defaults to None.
        """
        self._user_data_dir = (
            user_data_dir or get_platform_user_data_dir() / BPF_USER_DATA_DIR_NAME
        )
        if not self._user_data_dir.exists():
            init_user_data_dir(self._user_data_dir)
        self.log_file = self._user_data_dir / BPF_LOG_FILE_NAME
        self.lancedb_path = self._user_data_dir / DataStoreEnum.LANCEDB
        self.kuzu_path = self._user_data_dir / DataStoreEnum.KUZU
