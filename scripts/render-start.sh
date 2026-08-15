#!/usr/bin/env bash
set -euo pipefail

: "${PORT:=10000}"
export SERVER_PORT="${PORT}"
export ENABLE_AUTOPAUSE="false"
export ENABLE_AUTOSTOP="false"

exec /image/scripts/start "$@"
