#!/bin/bash

echo "======================================"
echo "Testing Monitoring Assistant Use Case"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env from .env.example"
    exit 1
fi

echo "✅ .env file found"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check dependencies
echo "Checking dependencies..."
cd ../..
if ! python3 -c "import dotenv" 2>/dev/null; then
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
fi

echo "✅ Dependencies OK"
echo ""

# Run the orchestrator
echo "======================================"
echo "Running Monitoring Assistant Orchestrator"
echo "======================================"
echo ""

cd use-cases/monitoring-assistant
python3 monitoring_orchestrator.py
