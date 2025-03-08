import os
import platform
import tomllib
from pathlib import Path
from typing import Any

import tomli_w

SYSTEM = platform.system()

LINUX_CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
WINDOWS_CONFIG_DIR = Path(os.environ.get("APPDATA", "~/AppData/Roaming")).expanduser()
MACOS_CONFIG_DIR = Path("~/Library/Application Support").expanduser()

BPF_CONFIG_DIR_NAME = "blueprintflow"
BPF_SETTINGS_FILE_NAME = "settings.toml"


def get_system_config_dir() -> Path:
    """Retrieve the system configuration directory based on the operating system.

    This function determines the appropriate configuration directory for the
    current operating system. If the operating system is not supported, a
    ValueError is raised.

    Raises:
        ValueError: If the operating system is not supported.

    Returns:
        Path: The path to the system configuration directory.
    """
    match SYSTEM:
        case "Darwin":
            config_dir = MACOS_CONFIG_DIR
        case "Linux":
            config_dir = LINUX_CONFIG_DIR
        case "Windows":
            config_dir = WINDOWS_CONFIG_DIR
        case _:
            msg = f"Unsupported operating system: {SYSTEM}"
            raise ValueError(msg)
    return config_dir


def get_main_config_dir() -> Path:
    """Retrieve the main configuration directory for BlueprintFlow based on the system.

    This function returns the main configuration directory for BlueprintFlow. If the
    directory does not exist, it is initialized.

    Returns:
        Path: The path to the main configuration directory.
    """
    config_dir = get_system_config_dir() / BPF_CONFIG_DIR_NAME
    if not config_dir.exists():
        _init_config_dir(config_dir)
    return config_dir


def _init_config_dir(config_dir: Path) -> None:
    """Initialize the configuration directory.

    This function ensures that the configuration directory exists by creating it
    if it does not already exist.

    Args:
        config_dir (Path): The path to the configuration directory.
    """
    # NOTE: ensure config_dir exists from this point forward
    config_dir.mkdir(parents=True, exist_ok=True)


def get_main_config_file() -> Path:
    """Retrieve the main settings file for BlueprintFlow based on the system.

    This function returns the path to the main settings file for BlueprintFlow.

    Returns:
        Path: The path to the settings file.
    """
    return get_main_config_dir() / BPF_SETTINGS_FILE_NAME


def read_config_file(filepath: Path) -> dict[str, Any]:
    """Read the BlueprintFlow settings file.

    This function reads the settings file at the specified path and returns the
    settings as a dictionary.

    Args:
        filepath (Path): The path to the settings file.

    Returns:
        dict[str, Any]: A dictionary containing the settings.
    """
    with filepath.open("rb") as file:
        return tomllib.load(file)


def save_main_config_file(settings: dict) -> None:
    """Save the BlueprintFlow settings to the main configuration file.

    This function saves the provided settings dictionary to the main configuration
    file for BlueprintFlow.

    Args:
        settings (dict): The settings dictionary to save.
    """
    with get_main_config_file().open("wb") as file:
        tomli_w.dump(settings, file)
