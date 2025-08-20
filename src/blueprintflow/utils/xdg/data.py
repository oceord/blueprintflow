import shutil
from pathlib import Path

from blueprintflow.utils.xdg.constants import (
    BPF_LANCEDB_DIR_NAME,
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


class UserData:
    """Manages user data directories and files.

    This class handles the initialization and management of user data directories
    and files, including the log file and embedded data files. It ensures that
    the necessary directories and files are created and accessible.

    Attributes:
        user_data_dir (Path): The path to the user data directory.
        log_file (Path): The path to the log file within the user data directory.
        lancedb_path (Path): The path to the LanceDB file within the user data
            directory.
    """

    def __init__(
        self, user_data_dir: Path | None = None, *, reset_if_exists: bool = False
    ) -> None:
        """Initialize the UserData instance.

        This constructor initializes the user data directory and ensures that
        the necessary files and subdirectories are created. If a user data directory
        is not provided, it defaults to the platform-specific user data directory.
        The directory may be reinitialized if reset_if_exists is True.

        Args:
            user_data_dir (Path, optional): The path to the user data directory.
                If not provided, the default platform-specific user data directory is
                used. Defaults to None.
            reset_if_exists (bool, optional): If True, reinitialize the user data
                directory. Defaults to False.
        """
        self.user_data_dir = (
            user_data_dir or get_platform_user_data_dir() / BPF_USER_DATA_DIR_NAME
        )
        self.log_file = self.user_data_dir / BPF_LOG_FILE_NAME
        self.lancedb_path = self.user_data_dir / BPF_LANCEDB_DIR_NAME
        if not self.user_data_dir.exists():
            self._init_user_data_dir()
        elif reset_if_exists:
            self.reset()

    def _init_user_data_dir(self) -> None:
        """Initialize the user data directory.

        This function ensures that the user data directory exists by creating it
        if it does not already exist.

        Args:
            data_dir (Path): The path to the user data directory.
        """
        self.user_data_dir.mkdir(parents=True, exist_ok=True)

    def reset(self) -> None:
        """Reset the user data directory to its initial state.

        This method removes the existing user data directory and all its contents,
        then reinitializes it as an empty directory. This is useful for cleaning up
        or resetting the state of the user data directory, such as during testing
        or when starting fresh.

        Note:
            This operation is irreversible and will delete all files and
            subdirectories within the user data directory.
        """
        shutil.rmtree(self.user_data_dir, ignore_errors=True)
        self._init_user_data_dir()
