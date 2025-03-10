#!/usr/bin/env bash
[[ $* =~ \S?\-\-debug\S? ]] && set -o xtrace
set -o errexit
set -o nounset
set -o pipefail

SYS_COMMON_PACKAGES=(
    gnupg2
    make
)
PIP_BUILD_PACKAGES=(
    build
)
SYS_DEV_PACKAGES=()
PIP_DEV_PACKAGES=(
    mypy
    pipenv
    ruff
    tox
)
PYENV_VERSIONS=(
    3.12
    3.13
)
CMD_SYS_INSTALL="apt-get update && apt-get install --no-install-recommends -y"
CMD_SYS_CLEANUP="apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*"
CMD_PIP_INSTALL="pip install --no-cache-dir"
CMD_PIPX_INSTALL="pipx install --pip-args=--no-cache-dir"
CMD_PYENV="$HOME/.pyenv/bin/pyenv"

usage() {
    echo "
Usage: $(basename "${BASH_SOURCE[0]}") [-h|--help] [--debug] [--install-system-common-packages] [--install-system-dev-packages] [--install-pip-build-packages] [--install-pip-dev-packages] [--use-pipx]

Script to install meta-dependencies for blueprintflow.
NOTE: meta-dependencies are dependencies of the dependencies.

Available options:

-h, --help                          Print this help and exit
--debug                             Enable debug trace
--install-system-common-packages    Install common packages (system package manager)
--install-system-dev-packages       Install development packages (system package manager)
--install-pip-build-packages            Install build packages (pip)
--install-pip-dev-packages              Install development packages (pip)
--use-pipx                          Use pipx instead of pip
"
    exit
}

msg() {
    echo >&2 -e "${1-}"
}

die() {
    local msg=$1
    local code=${2-1}
    msg "$msg"
    exit "$code"
}

parse_params() {
    INSTALL_SYS_COMMON_PACKAGES=0
    INSTALL_SYS_DEV_PACKAGES=0
    INSTALL_PIP_DEV_PACKAGES=0
    INSTALL_PIP_BUILD_PACKAGES=0
    INSTALL_PYENV=0
    INSTALL_PYENV_VERSIONS=0
    while :; do
        case "${1-}" in
        -h | --help) usage ;;
        --debug) ;;
        --install-system-common-packages) INSTALL_SYS_COMMON_PACKAGES=1 ;;
        --install-pip-build-packages) INSTALL_PIP_BUILD_PACKAGES=1 ;;
        --install-system-dev-packages) INSTALL_SYS_DEV_PACKAGES=1 ;;
        --install-pip-dev-packages) INSTALL_PIP_DEV_PACKAGES=1 ;;
        --install-pyenv) INSTALL_PYENV=1 ;;
        --install-pyenv-versions) INSTALL_PYENV_VERSIONS=1 ;;
        --use-pipx) CMD_PIP_INSTALL="$CMD_PIPX_INSTALL" ;;
        -?*) die "Unknown option: $1" ;;
        *) break ;;
        esac
        shift
    done
    return 0
}

parse_params "$@"

if ((INSTALL_SYS_COMMON_PACKAGES && ${#SYS_COMMON_PACKAGES[@]})); then
    eval "$CMD_SYS_INSTALL ${SYS_COMMON_PACKAGES[*]@Q}"
fi
if ((INSTALL_SYS_DEV_PACKAGES && ${#SYS_DEV_PACKAGES[@]})); then
    eval "$CMD_SYS_INSTALL ${SYS_DEV_PACKAGES[*]@Q}"
fi
if ((INSTALL_PIP_BUILD_PACKAGES && ${#PIP_BUILD_PACKAGES[@]})); then
    for package in "${PIP_BUILD_PACKAGES[@]}"; do
        eval "$CMD_PIP_INSTALL $package"
    done
fi
if ((INSTALL_PIP_DEV_PACKAGES && ${#PIP_DEV_PACKAGES[@]})); then
    for package in "${PIP_DEV_PACKAGES[@]}"; do
        eval "$CMD_PIP_INSTALL $package"
    done
fi
if ((INSTALL_PYENV)); then
    sudo apt-get update -y
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev curl git \
        libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
fi
if ((INSTALL_PYENV_VERSIONS && ${#PYENV_VERSIONS[@]})); then
    for version in "${PYENV_VERSIONS[@]}"; do
        eval "$CMD_PYENV install --skip-existing $version"
        eval "$CMD_PYENV global $version"
    done
fi
if ((INSTALL_SYS_COMMON_PACKAGES || INSTALL_SYS_DEV_PACKAGES)); then
    eval "$CMD_SYS_CLEANUP"
fi
