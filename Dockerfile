# LexCraft AI — single-container deployment (built/tested with Podman).
# `Dockerfile` (Render/BuildKit entry point) and `Containerfile` (Podman's
# native default) are identical on purpose — keep them in sync.
#
# ONE container runs all three processes:
#   nginx (public $PORT) ──► Streamlit UI (internal 8501, WebSocket-capable)
#                    └────► FastAPI   (internal 8000, /health + /api/*)
#
# Secrets are NEVER baked into this image: GEMINI_API_KEY is injected at
# runtime by the hosting platform or via `podman run --env-file`.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080

# nginx = reverse proxy (public port), supervisor = multi-process manager,
# gettext = envsubst for the nginx port template, curl = healthcheck.
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx supervisor gettext curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application source (build context excludes .env/.venv/caches via .containerignore)
COPY backend/ backend/
COPY frontend/ frontend/
COPY tests/ tests/
COPY assets/ assets/
COPY .streamlit/ .streamlit/
COPY pytest.ini .

# Proxy + process-manager configuration
COPY deploy/nginx.conf.template /etc/nginx/nginx.conf.template
COPY deploy/supervisord.conf /etc/supervisor/conf.d/lexcraft.conf
COPY deploy/start.sh /app/start.sh
RUN chmod +x /app/start.sh && rm -f /etc/nginx/sites-enabled/default

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=25s --retries=3 \
    CMD curl -sf "http://127.0.0.1:${PORT}/health" || exit 1

CMD ["/app/start.sh"]
