# ── Base image ───────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Keep Python output unbuffered so logs appear in real time
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# ── Dependencies ─────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Application files ─────────────────────────────────────────────────────────
COPY notebooks/ ./notebooks/

# ── Streamlit config ──────────────────────────────────────────────────────────
# Disable the browser-open behaviour and CORS warnings in containerised runs
RUN mkdir -p /root/.streamlit
RUN echo "[server]\nheadless = true\naddress = \"0.0.0.0\"\nport = 8501\nenableCORS = false\nenableXsrfProtection = false" \
    > /root/.streamlit/config.toml

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "notebooks/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]
