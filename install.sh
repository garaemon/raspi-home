#!/bin/bash

set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
cd "$script_dir"

PYTHON_VERSION=2.7.10

# source pyenv
export PYENV_ROOT=$HOME/.pyenv
export PATH=$PYENV_ROOT/bin:$PATH
eval "$(pyenv init -)"
export PYTHON_ROOT
PYTHON_ROOT="$(pyenv prefix)"

if ! pyenv versions | grep $PYTHON_VERSION; then
    pyenv install $PYTHON_VERSION
fi

pyenv shell $PYTHON_VERSION
make
