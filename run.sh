#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

PACKAGE_NAME="otterai"
VENV_DIR="myenv"

cd "$(dirname "$0")" || exit 1

echo "Setting up virtual environment..."
python -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate" || {
    echo "Failed to activate virtual environment"
    exit 1
}

echo "Installing dependencies from pyproject.toml..."
pip install --upgrade pip
pip install .[dev]

pre-commit install
pre-commit run --all-files

echo "Virtual environment '$VENV_DIR' is ready with dependencies installed."

echo "Running unit tests with coverage (skipping integration tests to avoid rate limits)..."
pytest -s \
    --cov="$PACKAGE_NAME" \
    --cov-report=term-missing \
    --cov-report=lcov:lcov.info \
    --cov-report=xml:cov.xml \
    -m "not integration" || {
    echo "Tests failed. Exiting..."
    exit 1
}

echo "⚠️  Note: Integration tests skipped to avoid 429 rate limit errors."
echo "   Run individual integration tests manually if needed:"
echo "   pytest tests/test_otterai.py::test_get_user -s"
echo "Coverage reports generated: lcov.info and cov.xml in the root directory."

echo "Starting the application..."
python main.py
