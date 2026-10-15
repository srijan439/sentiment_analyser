FROM python:3.11-slim

# Prevent Python from writing .pyc files and disable Streamlit telemetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# Create a non-root application user
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -m appuser

# 1. Install PyTorch CPU first to avoid downloading 5GB+ CUDA libraries
RUN pip install --no-cache-dir "torch>=2.2,<3" --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple

# 2. Install remaining runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy model files first (caches heavy 268MB weights layer)
COPY --chown=appuser:appuser model/ /app/model/

# 4. Copy app code (changes here won't invalidate model layer)
COPY --chown=appuser:appuser app/ /app/app/

USER appuser

EXPOSE 8501
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["python", "-m", "streamlit", "run", "app/app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
