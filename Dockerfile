FROM python:3.14-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 1. Install build dependencies BEFORE copying code or running uv sync
# This mirrors what Google Cloud Build has by default
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    # Essential for Rust/C extensions
    gcc \
    g++ \
    make \
    clang \
    pkg-config \
    # Specific headers often needed by libsql/rust crates
    libssl-dev \
    libzstd-dev \
    liblz4-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked --no-dev

CMD ["uv", "run", "src/main.py"]
