#!/bin/bash
# Run Nexus Dashboard Locally

echo "=========================================="
echo "Starting Nexus Dashboard"
echo "=========================================="
echo ""
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop the server"
echo "=========================================="
echo ""

cd "$(dirname "$0")/dashboard/api"
python3 -m uvicorn main:app --port 8000 --host 127.0.0.1 --reload
