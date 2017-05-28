#!/bin/bash

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 target-ip deploy-directory" >&2
    exit 1
fi

TARGET_IP=$1
TARGET_DIR=$2

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
cd "$script_dir"

git ls-files -z | rsync --files-from - --copy-links -av0 . "$TARGET_IP":"$TARGET_DIR"
scp .cache-${SPOTIPY_USER} "$TARGET_IP":"$TARGET_DIR"
rsync -avz ~/.config/raspi_home/ "$TARGET_IP":.config/raspi_home/
rsync -avz ~/.raspi-home-secrets/ "$TARGET_IP":.raspi-home-secrets/
unset LC_ALL
ssh "$TARGET_IP" "$TARGET_DIR"/install.sh
ssh "$TARGET_IP" "$TARGET_DIR"/kill.sh
ssh "$TARGET_IP" "$TARGET_DIR"/run.sh
