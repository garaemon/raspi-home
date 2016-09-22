#!/bin/bash

set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
cd "$script_dir/"..

title_echo() {
    LIGHT_BLUE='\033[0;36m'
    DEFAULT='\033[0;39m'
    echo -e "$LIGHT_BLUE" "$@" "$DEFAULT"
}


title_echo ">> checking yaml syntax"
yamllint ansible/raspi3.yaml
ansible-playbook  ansible/raspi3.yaml --syntax-check
title_echo "<< yaml OK"

title_echo ">> checking python syntax"
find . -name .venv -prune -type f -or -name '*.py' -type f -exec \
     pep8 --ignore=E402 --show-source --max-line-length=100 {} \;
title_echo "<< python OK"

title_echo ">> checking shell syntax"
find . -name .venv -prune -type f -or -name '*.sh' -type f -exec \
     shellcheck {} \;
title_echo "<< shell OK"
