# How to Run Locally

## Quick Start

### Terminal 1 - Backend API:
```bash
cd dashboard/api
python3 -m uvicorn main:app --port 8000 --host 127.0.0.1
```

### Terminal 2 - Frontend:
```bash
cd dashboard/web
npm run dev
```

## Access URLs

- **Frontend Dashboard**: http://localhost:3000 (or check terminal output)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Troubleshooting

If you get "Operation not permitted" errors:

1. **Try different ports:**
   - Backend: Change `--port 8000` to `--port 8888` or `--port 5000`
   - Frontend: Vite will auto-select an available port

2. **Check if ports are in use:**
   ```bash
   lsof -i :8000
   lsof -i :3000
   ```

3. **Run without reload (if reload causes issues):**
   ```bash
   python3 -m uvicorn main:app --port 8000 --host 127.0.0.1
   # (remove --reload flag)
   ```

4. **Check macOS Firewall:**
   - System Settings → Network → Firewall
   - Make sure it's not blocking local connections

## What's Running

- **Backend**: FastAPI server serving mock data
- **Frontend**: Vite dev server with React
- **Data**: All data is generated locally (no database needed)
