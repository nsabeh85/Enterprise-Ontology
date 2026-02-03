# Nexus Dashboard - Local Development --

Simple dashboard for query rewriter analytics using mock data.

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+

### Setup

1. **Install Python dependencies:**
```bash
pip install -r dashboard/api/requirements.txt
```

2. **Install frontend dependencies:**
```bash
cd dashboard/web
npm install
cd ../..
```

### Run

**Terminal 1 - Backend API:**
```bash
cd dashboard/api
python3 -m uvicorn main:app --port 8000 --host 127.0.0.1 --reload
```

**Terminal 2 - Frontend:**
```bash
cd dashboard/web
npm run dev
```

**Access:**
- Dashboard: http://localhost:5173
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
├── dashboard/
│   ├── api/              # FastAPI backend
│   │   ├── main.py       # API entry point
│   │   ├── data.py       # Mock data generator
│   │   └── services/
│   │       └── metrics_service.py  # Metrics calculations
│   └── web/              # React frontend
│       └── src/          # React components
```

## Notes

- Uses mock data for local development
- No database or external services required
- All data is generated on startup
