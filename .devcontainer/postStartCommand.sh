#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

make pipenv-dev-install

./scripts/install_meta_packages.sh --install-pyenv-versions
