import os
import platform
from pathlib import Path

SYSTEM = platform.system()

# User Configuration

LINUX_USER_CONFIG_DIR = Path(
    os.environ.get("XDG_CONFIG_HOME", "~/.config")
).expanduser()
MACOS_USER_CONFIG_DIR = Path("~/Library/Preferences").expanduser()
WINDOWS_USER_CONFIG_DIR = Path(
    os.environ.get("APPDATA", "~/AppData/Roaming")
).expanduser()

BPF_USER_CONFIG_DIR_NAME = "blueprintflow"
BPF_USER_SETTINGS_FILE_NAME = "settings.toml"

# User Data

LINUX_USER_DATA_DIR = Path(
    os.environ.get("XDG_DATA_HOME", "~/.local/share")
).expanduser()
MACOS_USER_DATA_DIR = Path("~/Library").expanduser()
WINDOWS_USER_DATA_DIR = Path(
    os.environ.get("LOCALAPPDATA", "~/AppData/Local")
).expanduser()

BPF_USER_DATA_DIR_NAME = "blueprintflow"
BPF_LOG_FILE_NAME = "blueprintflow.log"
