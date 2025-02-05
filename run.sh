#!/bin/bash

# exit immediately if any command fails
set -e  

echo "Starting setup..."

export PYTHONPATH=src:$PYTHONPATH

echo "Starting virtual enviornment"
python3 -m venv venv
source venv/bin/activate

echo "Starting mongodb"
brew services start mongodb-community

echo "Starting user window and admin window..."
python src/gui/main_window.py &
python admin/main.py &