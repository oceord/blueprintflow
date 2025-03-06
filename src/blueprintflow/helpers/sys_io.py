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
    """Get the system config directory.

    Raises:
        ValueError: system not supported

    Returns:
        Path: system config directory
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


def get_config_dir() -> Path:
    """Get the config directory for blueprintflow.

    Returns:
        Path: config directory
    """
    config_dir = get_system_config_dir() / BPF_CONFIG_DIR_NAME
    if not config_dir.exists():
        _init_config_dir(config_dir)
    return config_dir


def _init_config_dir(config_dir: Path) -> None:
    # NOTE: ensure config_dir exists from this point forward
    config_dir.mkdir(parents=True, exist_ok=True)


def get_config_file() -> Path:
    """Get blueprintflow settings file.

    Returns:
        Path | None: The path to the settings file or None if it does not exists.
    """
    return get_config_dir() / BPF_SETTINGS_FILE_NAME


def read_config_file(filepath: Path) -> dict[str, Any]:
    """Read the blueprintflow config file provided.

    Args:
        filepath (Path): the config filepath

    Returns:
        dict[str, Any]: the settings dictionary
    """
    with filepath.open("rb") as file:
        return tomllib.load(file)


def save_config_file(settings: dict) -> None:
    """Save blueprintflow settings according to the system.

    Args:
        settings (dict): settings dict to save
    """
    with get_config_file().open("wb") as file:
        tomli_w.dump(settings, file)
