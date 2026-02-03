#!/usr/bin/env python3
"""Simple script to start the backend server."""

import uvicorn
import sys
import os

# Change to API directory
os.chdir(os.path.join(os.path.dirname(__file__), 'dashboard', 'api'))

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Nexus Dashboard Backend")
    print("=" * 60)
    print("\nBackend will be available at: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop\n")
    print("=" * 60)
    
    try:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
