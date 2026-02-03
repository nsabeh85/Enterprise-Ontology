#!/bin/bash

# Start backend in background
cd "$(dirname "$0")/dashboard/api"
python3 -m uvicorn main:app --port 8000 --host 127.0.0.1 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend
cd "../web"
npm run dev &
FRONTEND_PID=$!

echo "=========================================="
echo "Services starting..."
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "=========================================="
echo ""
echo "Frontend will be available at: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop both services"
echo "=========================================="

# Wait for both processes
wait
