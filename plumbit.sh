#!/bin/bash
current_path=$( dirname ${BASH_SOURCE[0]}) && pwd
cd $current_path
source .venv/bin/activate
python3 app/plumbit.py
