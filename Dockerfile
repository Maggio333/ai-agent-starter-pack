# Dockerfile for AI Agent Starter Pack
# Multi-stage build for optimized image size

# ============================================================================
# Stage 1: Build stage
# ============================================================================
# Using Debian 12 (bookworm) for FFmpeg 6.x compatibility with PyAV 14.x
# Updated PyAV 14.x is compatible with FFmpeg 6.x/7.x
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies for building Python packages
# Note: pkg-config, libavcodec-dev, etc. are needed for faster-whisper (PyAV)
# FFmpeg 6.x from Debian 12 is compatible with PyAV 14.x
# Using BuildKit cache mount for apt cache to speed up subsequent builds
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libavdevice-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Note: pywin32 is Windows-only, so we exclude it for Linux Docker container
# Using BuildKit cache mount for pip cache to speed up subsequent builds
# Updated PyAV 14.x is compatible with FFmpeg 6.x
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    python -c "import sys; lines = [l for l in open('requirements.txt') if not l.strip().startswith('pywin32')]; open('requirements-docker.txt', 'w').writelines(lines)" && \
    pip install -r requirements-docker.txt

# ============================================================================
# Stage 2: Runtime stage
# ============================================================================
# Using Debian 12 (bookworm) base image for FFmpeg 6.x
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV API_HOST=0.0.0.0
ENV API_PORT=8080

# Run application
CMD ["python", "main_fastapi.py"]

