FROM ubuntu:22.04 as builder

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIPENV_VENV_IN_PROJECT=1

ARG PYPI_MIRROR=https://pypi.org/simple

WORKDIR /app

# Install only necessary build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3.10-venv && \
    rm -rf /var/lib/apt/lists/*

# Install pipenv and dependencies
COPY Pipfile* ./
RUN pip3 install --no-cache-dir -i ${PYPI_MIRROR} pipenv && \
    pipenv sync --pypi-mirror ${PYPI_MIRROR}

# Final stage
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Hong_Kong \
    TOKEN="" \
    CAPTCHA_SOLVER_CONFIG="{}" \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-venv && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment and application files
COPY --from=builder /app/.venv ./.venv
COPY . .

# Create data directory for logs
RUN mkdir -p /app/data && \
    chmod -R 777 /app/data

HEALTHCHECK --interval=30s --timeout=10s --retries=1 \
    CMD if grep -q Exception /app/data/output.log; then exit 1; else exit 0; fi

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["/bin/sh", "-c", "pipenv run python -m lokbot $TOKEN $CAPTCHA_SOLVER_CONFIG 2>&1 | tee -a /app/data/output.log"]
