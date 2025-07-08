#!/bin/bash

# OtterAI Interactive Performance Script
# This script provides an easy way to run the OtterAI interactive runner

set -e

echo "🦦 OtterAI Interactive Runner"
echo "============================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your OtterAI credentials:"
    echo ""
    echo "OTTERAI_USERNAME=your_username"
    echo "OTTERAI_PASSWORD=your_password"
    echo "TEST_OTTERAI_SPEECH_OTID=your_test_speech_otid"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "⚠️  No virtual environment found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -e .
else
    # Activate virtual environment
    if [ -d "venv" ]; then
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
fi

# Check if dependencies are installed
if ! python -c "import otterai" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -e .
fi

# Check if rich is installed (needed for interactive runner)
if ! python -c "import rich" 2>/dev/null; then
    echo "📦 Installing development dependencies (including rich)..."
    pip install -e ".[dev]"
fi

# Run the interactive script
echo "🚀 Starting OtterAI Interactive Runner..."
echo ""
python interactive_runner.py