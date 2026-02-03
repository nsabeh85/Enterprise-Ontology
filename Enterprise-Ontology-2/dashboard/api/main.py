"""
Nexus Dashboard API - Local Development Version
"""

from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from services.metrics_service import MetricsService

app = FastAPI(
    title="Nexus Dashboard API",
    description="Local development API with mock data",
    version="1.0.0",
)

# CORS - allow all origins for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize metrics service
metrics_service = MetricsService()

# Static files (for production build)
STATIC_DIR = Path(__file__).parent / "static"
INDEX_HTML = STATIC_DIR / "index.html"


@app.get("/")
async def root():
    """Serve React app or API info."""
    if INDEX_HTML.exists():
        return FileResponse(str(INDEX_HTML))
    return {
        "name": "Nexus Dashboard API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "note": "Using mock data for local development"
    }


@app.get("/api/status")
async def get_status():
    """API status endpoint."""
    return {
        "status": "running",
        "mode": "local",
        "dataSource": "mock_data",
        "lastSync": datetime.now().isoformat(),
        "cache_stats": {
            "rewriter_records": 100,
            "adoption_records": 200,
            "feedback_records": 60,
        }
    }


@app.get("/api/rewriter")
async def get_rewriter_metrics():
    """Get query rewriter metrics."""
    metrics = metrics_service.calculate_rewriter_metrics()
    metrics["metadata"] = {
        "generatedAt": datetime.now().isoformat(),
        "lastSync": datetime.now().isoformat(),
        "dataSource": "mock_data",
        "recordCount": 100,
    }
    return metrics


@app.get("/api/adoption")
async def get_adoption_metrics():
    """Get adoption metrics."""
    metrics = metrics_service.calculate_adoption_metrics()
    metrics["metadata"] = {
        "generatedAt": datetime.now().isoformat(),
        "lastSync": datetime.now().isoformat(),
        "dataSource": "mock_data",
        "recordCount": 200,
    }
    return metrics


@app.get("/api/feedback")
async def get_feedback_metrics():
    """Get feedback metrics."""
    metrics = metrics_service.calculate_feedback_metrics()
    metrics["metadata"] = {
        "generatedAt": datetime.now().isoformat(),
        "lastSync": datetime.now().isoformat(),
        "dataSource": "mock_data",
        "recordCount": 60,
    }
    return metrics


# Serve static files if they exist
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="frontend")


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    """SPA fallback for React Router."""
    if INDEX_HTML.exists():
        return FileResponse(str(INDEX_HTML))
    return {"error": "Not Found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
