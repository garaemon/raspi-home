#!/bin/bash

set -e

PROCESS_NAME=run_raspi_server.py
pgrep -f $PROCESS_NAME && pkill -f $PROCESS_NAME
exit 0
