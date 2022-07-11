#!/bin/bash

cd $( dirname ${BASH_SOURCE[0]}) && pwd
source .venv/bin/activate
python3 plumbit.py
