# Quick Start Guide

## The Problem
You're getting "connection failed" because **both services need to be running at the same time**.

## Solution - Start Both Services

### Terminal 1: Backend API
```bash
cd /Users/NSabeh/Desktop/nexus-dashboard/Enterprise-Ontology-2/dashboard/api
python3 -m uvicorn main:app --port 8000 --host 127.0.0.1
```

**Wait for:** `Application startup complete` message

**Test it:** Open http://localhost:8000/api/status in browser - should show JSON

### Terminal 2: Frontend
```bash
cd /Users/NSabeh/Desktop/nexus-dashboard/Enterprise-Ontology-2/dashboard/web
npm run dev
```

**Wait for:** `Local: http://localhost:3000` message (or similar)

### Open Browser
Open the URL shown in Terminal 2 (usually http://localhost:3000)

## Troubleshooting

### If you see "Operation not permitted"
This is a macOS security restriction. Try:

1. **Run commands directly in Terminal** (not through scripts)
2. **Use different ports:**
   ```bash
   # Backend on port 8888
   python3 -m uvicorn main:app --port 8888 --host 127.0.0.1
   
   # Then update vite.config.js proxy target to http://127.0.0.1:8888
   ```

### Check if services are running:
```bash
# Backend
curl http://localhost:8000/api/status

# Should return JSON, not "connection refused"
```

### Common Issues:

1. **"Connection refused"** = Service not running
2. **"Operation not permitted"** = macOS security restriction
3. **"Port already in use"** = Another process using the port
4. **Frontend shows "Failed to fetch"** = Backend not running or wrong port

## What Should Happen

1. ✅ Backend starts → Shows "Application startup complete"
2. ✅ Frontend starts → Shows "Local: http://localhost:XXXX"
3. ✅ Browser opens → Dashboard loads with data

If any step fails, check the terminal output for error messages.
