#!/bin/bash
set -e

python migrator.py 2>&1 >/tmp/dm.log &
python main.py
