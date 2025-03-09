import tomllib
from pathlib import Path
from typing import Any

import tomli_w

from blueprintflow.helpers.xdg.constants import (
    BPF_USER_CONFIG_DIR_NAME,
    BPF_USER_SETTINGS_FILE_NAME,
    LINUX_USER_CONFIG_DIR,
    MACOS_USER_CONFIG_DIR,
    SYSTEM,
    WINDOWS_USER_CONFIG_DIR,
)


def get_platform_user_config_dir() -> Path:
    """Retrieve the user configuration directory for the current platform.

    This function determines the appropriate user configuration directory for the
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


def init_user_config_dir(config_dir: Path) -> None:
    """Initialize the user configuration directory.

    This function ensures that the user configuration directory exists by creating it
    if it does not already exist.

    Args:
        config_dir (Path): The path to the user configuration directory.
    """
    config_dir.mkdir(parents=True, exist_ok=True)


class UserConfig:
    """Manages user configuration directories and files.

    This class handles the initialization and management of user configuration
    directories and files, including the settings file. It ensures that the necessary
    directories and files are created and accessible.

    Attributes:
        _user_config_dir (Path): The path to the user configuration directory.
        user_config_file (Path): The path to the user configuration file within the user
            configuration directory.
    """

    def __init__(self, user_config_dir: Path | None = None) -> None:
        """Initialize the UserConfig instance.

        This constructor initializes the user configuration directory and ensures that
        the necessary files and subdirectories are created. If a user configuration
        directory is not provided, it defaults to the platform-specific user
        configuration directory.

        Args:
            user_config_dir (Path, optional): The path to the user config directory.
                If not provided, the default platform-specific user config directory is
                used. Defaults to None.
        """
        self._user_config_dir = (
            user_config_dir or get_platform_user_config_dir() / BPF_USER_CONFIG_DIR_NAME
        )
        if not self._user_config_dir.exists():
            init_user_config_dir(self._user_config_dir)
        self.user_config_file = self._user_config_dir / BPF_USER_SETTINGS_FILE_NAME

    def read_user_config_file(self, filepath: Path | None = None) -> dict[str, Any]:
        """Read the user configuration file and return its contents as a dictionary.

        This method reads the user configuration file and parses its contents using the
        TOML format. The contents are returned as a dictionary. If no file path is
        provided, it defaults to the user configuration file path.

        Args:
            filepath (Path, optional): The path to the configuration file.
                If not provided, the default user configuration file path is used.
                Defaults to None.

        Returns:
            dict[str, Any]: A dictionary containing the parsed configuration settings.
        """
        config_file = filepath or self.user_config_file
        with config_file.open("rb") as file:
            return tomllib.load(file)

    def save_user_config_file(self, settings: dict) -> None:
        """Save the user configuration settings to the configuration file.

        This method writes the provided configuration settings to the user configuration
        file using the TOML format.

        Args:
            settings (dict): The configuration settings to save.
        """
        with self.user_config_file.open("wb") as file:
            tomli_w.dump(settings, file)
