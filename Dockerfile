# MemoryGuard Docker Image
# Usage: docker run -v $(pwd):/app ghcr.io/shadd0wtaka/memoryguard python -c "from memoryguard import MemoryGuard; ..."

FROM python:3.11-slim

LABEL maintainer="SHAdd0WTAka"
LABEL description="MemoryGuard - Modular Python Memory Monitoring"
LABEL org.opencontainers.image.source="https://github.com/SHAdd0WTAka/memoryguard"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    valgrind \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY pyproject.toml README.md ./
COPY memoryguard/ ./memoryguard/

# Install the package
RUN pip install --no-cache-dir -e ".[all]"

# Create non-root user
RUN useradd -m -u 1000 memoryguard && \
    chown -R memoryguard:memoryguard /app
USER memoryguard

# Default command
CMD ["python", "-c", "from memoryguard import MemoryGuard, __version__; print(f'MemoryGuard v{__version__} ready!')"]
