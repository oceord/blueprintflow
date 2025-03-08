import os
import platform
from pathlib import Path

from blueprintflow.core.model.embedded_data import EmbeddedDataEnum

SYSTEM = platform.system()

LINUX_USER_DATA_DIR = Path(
    os.environ.get("XDG_DATA_HOME", "~/.local/share")
).expanduser()
MACOS_USER_DATA_DIR = Path("~/Library").expanduser()
WINDOWS_USER_DATA_DIR = Path(
    os.environ.get("LOCALAPPDATA", "~/AppData/Local")
).expanduser()

BPF_USER_DATA_DIR_NAME = "blueprintflow"


def get_platform_user_data_dir() -> Path:
    """Retrieve the user data directory for the current platform.

    This function determines the appropriate data directory for the
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


def get_user_data_dir() -> Path:
    """Retrieve the user data directory for blueprintflow.

    This function returns the user data directory for blueprintflow. If the
    directory does not exist, it is initialized.

    Returns:
        Path: The path to the user data directory.
    """
    data_dir = get_platform_user_data_dir() / BPF_USER_DATA_DIR_NAME
    if not data_dir.exists():
        _init_user_data_dir(data_dir)
    return data_dir


def _init_user_data_dir(data_dir: Path) -> None:
    """Initialize the user data directory.

    This function ensures that the user data directory exists by creating it
    if it does not already exist.

    Args:
        data_dir (Path): The path to the user data directory.
    """
    # NOTE: ensure data_dir exists from this point forward
    data_dir.mkdir(parents=True, exist_ok=True)


def get_user_data_file(datafile: EmbeddedDataEnum) -> Path:
    """Retrieve the path to a specific user data file based on the provided enum.

    This function constructs the path to a user data file by combining the user data
    directory with the specified data file enum. The resulting path points to the
    location of the data file within the user's data directory.

    Args:
        datafile (EmbeddedDataEnum): An enum representing the specific data file to
            retrieve.

    Returns:
        Path: The path to the specified user data file.
    """
    return get_user_data_dir() / datafile
