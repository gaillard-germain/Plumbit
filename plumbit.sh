#!/bin/bash
current_path=$( dirname ${BASH_SOURCE[0]}) && pwd
cd "$current_path" || exit

if [ ! -d ".venv/" ]; then
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
else
  source .venv/bin/activate
fi

python3 run.py
