"""
Sentiment Analyzer Entry Point
Exposes the FastAPI application and allows direct execution with `python app/app.py`.
"""

import os
import sys

# Ensure the project root directory is first in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import uvicorn

try:
    from app.main import app
except (ImportError, ModuleNotFoundError):
    from main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"🚀 Starting BERT Sentiment Analyzer on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port, reload=False)
