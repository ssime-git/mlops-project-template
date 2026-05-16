# Training Container Dockerfile
# Phase 1: Containerized training pipeline

FROM python:3.10-slim

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy the entire workspace for uv sync
COPY pyproject.toml .
COPY src/ ./src/
COPY configs/ ./configs/

# Install workspace packages (all dependencies including dev for debugging)
RUN uv sync --no-dev

# Copy data (can be mounted instead in production)
COPY data/ ./data/

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Default command (can be overridden)
CMD ["python", "-m", "training", "train"]