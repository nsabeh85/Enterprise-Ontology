#!/bin/bash
# Check if services are running

echo "=========================================="
echo "Checking Service Status"
echo "=========================================="
echo ""

# Check backend
echo "Backend (port 8000):"
if curl -s http://127.0.0.1:8000/api/status > /dev/null 2>&1; then
    echo "  ✅ RUNNING"
    curl -s http://127.0.0.1:8000/api/status | python3 -m json.tool 2>/dev/null | head -5
else
    echo "  ❌ NOT RUNNING"
    echo "  Start with: cd dashboard/api && python3 -m uvicorn main:app --port 8000 --host 127.0.0.1"
fi

echo ""
echo "Frontend (port 3000):"
if curl -s http://127.0.0.1:3000 > /dev/null 2>&1; then
    echo "  ✅ RUNNING"
else
    echo "  ❌ NOT RUNNING"
    echo "  Start with: cd dashboard/web && npm run dev"
fi

echo ""
echo "Frontend (port 5173):"
if curl -s http://127.0.0.1:5173 > /dev/null 2>&1; then
    echo "  ✅ RUNNING"
else
    echo "  ❌ NOT RUNNING"
fi

echo ""
echo "=========================================="
