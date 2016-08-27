#!/bin/bash

set -e

script_dir=$(cd $(dirname $BASH_SOURCE); pwd)
cd $script_dir

PYTHON_VERSION=2.7.10

# source pyenv
export PYENV_ROOT=$HOME/.pyenv
export PATH=$PYENV_ROOT/bin:$PATH
eval "$(pyenv init -)"
export PYTHON_ROOT=$(pyenv prefix)

if ! pyenv versions | grep $PYTHON_VERSION; then
    pyenv install $PYTHON_VERSION
fi

# setup virtualenv
if [ ! -e raspi-server/env ] ; then
    (cd raspi-server &&
     pyenv local $PYTHON_VERSION &&
     virtualenv env)
fi

cd raspi-server

source env/bin/activate
pip install -r requirements.txt
