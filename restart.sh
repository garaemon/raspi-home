#!/bin/bash

# This script restart server process only if process is dead.
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
process_name=run_raspi_server.py
pgrep -f "${process_name}" >/dev/null

if ! pgrep -f "${process_name}" >/dev/null; then
    "${script_dir}"/run.sh
fi
