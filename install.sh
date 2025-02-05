#!/bin/bash

# exit immediately if any command fails
set -e  

echo "Starting setup..."

# install MongoDB Community Edition if not installed
if ! brew list | grep -q "mongodb-community"; then
    echo "Installing MongoDB Community Edition..."
    brew tap mongodb/brew
    brew install mongodb-community
fi

# start mongo
echo "Starting MongoDB..."
brew services start mongodb-community

# create and activate virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# install tkinter
python3 -c "import tkinter" || (echo "Installing Tkinter..." && brew install python-tk)

# add everything to path so it can find files
export PYTHONPATH=src:$PYTHONPATH         

# install python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
fi

echo "Starting user window and admin window..."
python src/gui/main_window.py &
python admin/main.py &

echo "Setup complete!"
