#!/bin/sh
# LexCraft AI — container entrypoint.
# 1. Render nginx config with the platform-assigned $PORT (default 8080)
# 2. Launch all three processes via supervisord
set -e

export PORT="${PORT:-8080}"
echo "[start.sh] public port: ${PORT}"

envsubst '${PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec supervisord -c /etc/supervisor/conf.d/lexcraft.conf
