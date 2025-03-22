#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

sudo chown vscode:vscode .venv
sudo chown -R vscode:vscode /home/vscode

sudo ./scripts/install_meta_packages.sh \
    --install-system-common-packages \
    --install-system-dev-packages

./scripts/install_meta_packages.sh --use-pipx \
    --install-pip-dev-packages

./scripts/install_meta_packages.sh --install-pyenv

make set-up-git
