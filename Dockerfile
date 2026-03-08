# ── Build Stage ───────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Runtime Stage ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

LABEL maintainer="Saeed Rafay <saeedrafay.com>"
LABEL description="FinComplianceAgent — Multi-Agent Regulatory Intelligence"
LABEL version="1.0.0"

WORKDIR /app

# Ensure project root is on the Python path so `graph` and `agents` are importable
ENV PYTHONPATH=/app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY agents/ ./agents/
COPY graph/ ./graph/
COPY ui/ ./ui/
COPY main.py .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from graph.compliance_graph import build_compliance_graph; build_compliance_graph()" || exit 1

# Default: run Streamlit UI
CMD ["streamlit", "run", "ui/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
