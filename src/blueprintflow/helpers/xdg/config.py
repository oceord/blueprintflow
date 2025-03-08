import os
import platform
import tomllib
from pathlib import Path
from typing import Any

import tomli_w

SYSTEM = platform.system()

LINUX_USER_CONFIG_DIR = Path(
    os.environ.get("XDG_CONFIG_HOME", "~/.config")
).expanduser()
MACOS_USER_CONFIG_DIR = Path("~/Library/Preferences").expanduser()
WINDOWS_USER_CONFIG_DIR = Path(
    os.environ.get("APPDATA", "~/AppData/Roaming")
).expanduser()

BPF_USER_CONFIG_DIR_NAME = "blueprintflow"
BPF_USER_SETTINGS_FILE_NAME = "settings.toml"


def get_platform_user_config_dir() -> Path:
    """Retrieve the user configuration directory for the current platform.

    This function determines the appropriate configuration directory for the
    current operating system. If the operating system is not supported, a
    ValueError is raised.

    Raises:
        ValueError: If the operating system is not supported.

    Returns:
        Path: The path to the system configuration directory.
    """
    match SYSTEM:
        case "Linux":
            config_dir = LINUX_USER_CONFIG_DIR
        case "Darwin":
            config_dir = MACOS_USER_CONFIG_DIR
        case "Windows":
            config_dir = WINDOWS_USER_CONFIG_DIR
        case _:
            msg = f"Unsupported operating system: {SYSTEM}"
            raise ValueError(msg)
    return config_dir


def get_user_config_dir() -> Path:
    """Retrieve the user configuration directory for BlueprintFlow based on the system.

    This function returns the user configuration directory for BlueprintFlow.
    If the directory does not exist, it is initialized.

    Returns:
        Path: The path to the user configuration directory.
    """
    config_dir = get_platform_user_config_dir() / BPF_USER_CONFIG_DIR_NAME
    if not config_dir.exists():
        _init_user_config_dir(config_dir)
    return config_dir


def _init_user_config_dir(config_dir: Path) -> None:
    """Initialize the user configuration directory.

    This function ensures that the user configuration directory exists by creating it
    if it does not already exist.

    Args:
        config_dir (Path): The path to the user configuration directory.
    """
    # NOTE: ensure config_dir exists from this point forward
    config_dir.mkdir(parents=True, exist_ok=True)


def get_user_config_file() -> Path:
    """Retrieve the user settings file for BlueprintFlow based on the system.

    This function returns the path to the user settings file for BlueprintFlow.

    Returns:
        Path: The path to the settings file.
    """
    return get_user_config_dir() / BPF_USER_SETTINGS_FILE_NAME


def read_user_config_file(filepath: Path | None) -> dict[str, Any]:
    """Read the user configuration file and return its contents as a dictionary.

    This function reads the configuration file specified by `filepath`.
    If `filepath` is not provided, it defaults to the user's configuration file path.
    The file is expected to be in TOML format.
    The contents of the file are parsed and returned as a dictionary.

    Args:
        filepath (Path, optional): The path to the configuration file. If not provided,
            the default user configuration file path is used. Defaults to None.

    Returns:
        dict[str, Any]: A dictionary containing the parsed configuration settings.
    """
    config_file = filepath or get_user_config_file()
    with config_file.open("rb") as file:
        return tomllib.load(file)


def save_user_config_file(settings: dict) -> None:
    """Save BlueprintFlow settings to the user configuration file based on the system.

    This function saves the provided settings dictionary to the user configuration
    file for BlueprintFlow.

    Args:
        settings (dict): The settings dictionary to save.
    """
    with get_user_config_file().open("wb") as file:
        tomli_w.dump(settings, file)
