# Troubleshooting Connection Issues

## Problem: "Connection Failed" Error

This usually means the services aren't running. Follow these steps:

### Step 1: Start the Backend

**Option A - Using Python script:**
```bash
cd /Users/NSabeh/Desktop/nexus-dashboard/Enterprise-Ontology-2
python3 start_backend.py
```

**Option B - Direct command:**
```bash
cd /Users/NSabeh/Desktop/nexus-dashboard/Enterprise-Ontology-2/dashboard/api
python3 -m uvicorn main:app --port 8000 --host 127.0.0.1
```

**Verify backend is running:**
- Open http://localhost:8000/api/status in your browser
- You should see JSON with status information

### Step 2: Start the Frontend

**In a NEW terminal window:**
```bash
cd /Users/NSabeh/Desktop/nexus-dashboard/Enterprise-Ontology-2/dashboard/web
npm run dev
```

**Note the URL shown** - it will be something like:
- http://localhost:3000
- http://localhost:5173
- or another port if those are taken

### Step 3: Open in Browser

Open the frontend URL shown in the terminal (usually http://localhost:3000)

## Common Issues

### "Port already in use"
Try a different port:
```bash
# Backend on different port
python3 -m uvicorn main:app --port 8888 --host 127.0.0.1

# Then update vite.config.js proxy target to http://localhost:8888
```

### "Operation not permitted"
This is a macOS security restriction. Try:
1. Running commands directly in Terminal (not through scripts)
2. Using different ports (8888, 5000, etc.)
3. Checking System Settings → Network → Firewall

### "Cannot connect to API"
1. Make sure backend is running (check http://localhost:8000/api/status)
2. Check the frontend terminal for the actual port it's using
3. Verify vite.config.js proxy target matches backend port

### Check if services are running:
```bash
# Check backend
lsof -ti:8000 && echo "Backend running" || echo "Backend NOT running"

# Check frontend
lsof -ti:3000 && echo "Frontend on 3000" || lsof -ti:5173 && echo "Frontend on 5173" || echo "Frontend NOT running"
```

## Quick Test

Test the backend directly:
```bash
curl http://localhost:8000/api/status
```

If this works, the backend is running correctly. The frontend just needs to connect to it.
