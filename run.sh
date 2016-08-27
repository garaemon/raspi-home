#!/bin/bash

set -e

script_dir=$(cd $(dirname $BASH_SOURCE); pwd)
cd $script_dir

cd python
source env/bin/activate
if [ -e $HOME/.slackbotrc ]; then
    source $HOME/.slackbotrc
fi
screen -S raspi-server -d -m run_raspi_server.py
