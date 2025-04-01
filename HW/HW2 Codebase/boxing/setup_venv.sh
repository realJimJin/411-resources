#!/bin/bash

VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment at $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
  source "$VENV_DIR/bin/activate"
  pip install --upgrade pip

  if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
    pip install pytest pytest-mock
  else
    echo "Error: $REQUIREMENTS_FILE not found."
    exit 1
  fi
else
  echo "Virtual environment already exists. Activating..."
  source "$VENV_DIR/bin/activate"
fi
