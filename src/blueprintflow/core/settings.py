import tomllib
from importlib import resources
from pathlib import Path
from typing import Any

from blueprintflow.core import defaults
from blueprintflow.core.model.settings import BlueprintFlowSettings
from blueprintflow.helpers.sys_io import (
    get_config_file,
    read_config_file,
    save_config_file,
)
from blueprintflow.helpers.validations import eq_struct

with resources.files(defaults).joinpath("settings.toml").open("rb") as file:
    default_settings = tomllib.load(file)


def load_settings(filepath: Path | None = None) -> BlueprintFlowSettings:
    """Load blueprintflow settings.

    Args:
        filepath (Path | None, optional): The filepath to load.
            If not provided the default settings will be used.
            Defaults to None.

    Returns:
        BlueprintFlowSettings: pydantic objective with the settings
    """
    __validate_settings_filepath(filepath)
    base_config_filepath = get_config_file()
    if not base_config_filepath.exists():
        save_config_file(default_settings)
    config_filepath = filepath or base_config_filepath
    settings_buffer = (
        read_config_file(config_filepath)
        if config_filepath is not None
        else default_settings
    )
    __validate_settings_dict(settings_buffer)
    return BlueprintFlowSettings(**settings_buffer)


def __validate_settings_filepath(filepath: Path | None) -> None:
    """Validate the filepath provided.

    Args:
        filepath (Path | None): the settings filepath

    Raises:
        ArgumentError: the file must be TOML
        ArgumentError: the path provided must be a file

    Examples:
        >>> __validate_settings_filepath(None)

        >>> __validate_settings_filepath(
        ...     Path("src/blueprintflow/core/defaults/settings.toml")
        ... )

        >>> __validate_settings_filepath(
        ...     Path("foo.toml")
        ... )
        Traceback (most recent call last):
            ...
        ValueError: 'filepath' must be an existing filepath

        >>> __validate_settings_filepath(
        ...     Path("src/blueprintflow/core/defaults/__init__.py")
        ... )
        Traceback (most recent call last):
            ...
        ValueError: 'filepath' must be a toml file
    """
    if filepath is not None and not filepath.is_file():
        msg = "'filepath' must be an existing filepath"
        raise ValueError(msg)
    if filepath is not None and filepath.suffix != ".toml":
        msg = "'filepath' must be a toml file"
        raise ValueError(msg)


def __validate_settings_dict(settings: dict[str, Any]) -> None:
    if not eq_struct(default_settings, settings):
        msg = "Loaded settings are structurally different from the default settings."
        raise ValueError(msg)
