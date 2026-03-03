#!/bin/bash
# Run Myntra automation tests - use these commands from project root.

cd "$(dirname "$0")"
source venv/bin/activate

echo "=== App launch tests (smoke) ==="
pytest tests/test_app_launch.py -v

echo ""
echo "=== All smoke tests ==="
pytest -m smoke -v
