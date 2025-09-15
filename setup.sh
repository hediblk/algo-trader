#!/bin/bash

echo "Removing old virtual environment if it exists..."

if [ -d ".venv" ]; then
echo "Old virtual environment found. Removing..."
    rm -rf .venv
fi

echo "Creating new virtual environment..."
python3 -m venv .venv

source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete. The virtual environment '.venv' is ready and dependencies are installed."
