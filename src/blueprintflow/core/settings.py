import tomllib
from importlib import resources
from pathlib import Path
from typing import Any

from blueprintflow.core import defaults
from blueprintflow.core.models.settings import BlueprintFlowSettings
from blueprintflow.helpers.validations import eq_struct
from blueprintflow.helpers.xdg.config import UserConfig

with resources.files(defaults).joinpath("settings.toml").open("rb") as file:
    default_settings = tomllib.load(file)


def load_settings(
    user_config: UserConfig | None = None, filepath: Path | None = None
) -> BlueprintFlowSettings:
    """Load BlueprintFlow settings from a specified file or use default settings.

    This function loads the BlueprintFlow settings from the provided file path.
    If no file path is provided, it uses the default settings.
    The function validates the file path and the settings dictionary before
    returning the settings as a `BlueprintFlowSettings` object.

    Args:
        user_config(UserConfig, optional): An optional UserConfig instance that
            specifies the user configuration directory and file. If not provided,
            a default UserConfig instance will be used. Defaults to None.
        filepath (Path, optional): The file path to load the settings from.
            If not provided, the default settings will be used. Defaults to None.

    Returns:
        BlueprintFlowSettings: A Pydantic object containing the loaded settings.

    Examples:
        >>> user_settings = load_settings()

        >>> file_settings = load_settings(
        ...     user_config=UserConfig(Path("~/.config/blueprintflow"))
        ... )

        >>> file_settings = load_settings(
        ...     filepath=Path("src/blueprintflow/core/defaults/settings.toml")
        ... )
    """
    __validate_settings_filepath(filepath)
    _user_config = user_config or UserConfig()
    if not _user_config.user_config_file.exists():
        _user_config.save_user_config_file(default_settings)
    settings_file = filepath or _user_config.user_config_file
    settings_buffer = (
        _user_config.read_user_config_file(settings_file)
        if settings_file is not None
        else default_settings
    )
    __validate_settings_dict(settings_buffer)
    return BlueprintFlowSettings(**settings_buffer)


def __validate_settings_filepath(filepath: Path | None) -> None:
    """Validate the provided settings file path.

    This function checks if the provided file path is a valid TOML file and exists.
    If the file path is invalid, it raises a ValueError with an appropriate error
    message.

    Args:
        filepath (Path, optional): The settings file path to validate.

    Raises:
        ValueError: If the file path is not an existing file.
        ValueError: If the file path does not point to a TOML file.

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
    """Validate the structure of the settings dictionary.

    This function checks if the provided settings dictionary has the same structure as
    the default settings. If the structures do not match, it raises a ValueError.

    Args:
        settings (dict[str, Any]): The settings dictionary to validate.

    Raises:
        ValueError: If the structure of the settings dictionary is different from the
            default settings.

    Examples:
        >>> __validate_settings_dict(default_settings)

        >>> __validate_settings_dict({})
        Traceback (most recent call last):
            ...
        ValueError: Loaded settings are structurally different from the default settings.
    """  # noqa: E501
    if not eq_struct(default_settings, settings):
        msg = "Loaded settings are structurally different from the default settings."
        raise ValueError(msg)
