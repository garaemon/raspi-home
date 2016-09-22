#!/bin/bash

set -e

script_dir=$(cd $(dirname $BASH_SOURCE); pwd)
cd $script_dir

source .venv/bin/activate
if [ -e $HOME/.slackbotrc ]; then
    source $HOME/.slackbotrc
fi
screen -S raspi-server -d -m ./bin/run_raspi_server.py
