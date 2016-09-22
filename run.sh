#!/bin/bash

set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
cd "$script_dir"

# shellcheck disable=SC1091
source .venv/bin/activate
if [ -e "$HOME"/.slackbotrc ]; then
    # shellcheck disable=SC1090
    source "$HOME"/.slackbotrc
fi
screen -S raspi-server -d -m ./bin/run_raspi_server.py
