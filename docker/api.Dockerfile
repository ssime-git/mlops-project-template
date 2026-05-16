# FastAPI Inference Service Dockerfile
# Phase 1: Containerized inference API

FROM python:3.10-slim

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy the entire workspace for uv sync (includes src/* packages)
COPY pyproject.toml .
COPY src/ ./src/

# Install workspace packages (production only, no dev dependencies)
RUN uv sync --no-dev

# Copy models after install (they change more often)
COPY models/ ./models/

# Set PYTHONPATH so imports work (src.api becomes importable)
ENV PYTHONPATH=/app

# Expose API port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]