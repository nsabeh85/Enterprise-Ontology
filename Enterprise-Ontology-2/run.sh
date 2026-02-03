#!/bin/bash
# Run Nexus Dashboard - Copy and paste this into your terminal

echo "=========================================="
echo "Starting Nexus Dashboard"
echo "=========================================="
echo ""

# Start backend
echo "Starting backend on port 8000..."
cd "$(dirname "$0")/dashboard/api"
python3 -m uvicorn main:app --port 8000 --host 127.0.0.1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check if backend started
if curl -s http://127.0.0.1:8000/api/status > /dev/null 2>&1; then
    echo "✅ Backend started successfully!"
    echo "   API: http://localhost:8000"
    echo "   Docs: http://localhost:8000/docs"
else
    echo "❌ Backend failed to start (check for port conflicts)"
    echo "   Try: python3 -m uvicorn main:app --port 8888 --host 127.0.0.1"
    exit 1
fi

echo ""
echo "Starting frontend..."
cd "../web"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo "Services starting..."
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "=========================================="
echo ""
echo "Frontend will be available at: http://localhost:3000"
echo "(Check terminal output for actual URL)"
echo ""
echo "Press CTRL+C to stop both services"
echo "=========================================="

# Wait for user interrupt
wait
