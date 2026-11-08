#!/usr/bin/env bash
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$DIR/.server.pid" ]; then
  kill "$(cat "$DIR/.server.pid")" 2>/dev/null && echo "[OK] Node dihentikan."
  rm -f "$DIR/.server.pid"
else
  pkill -f app.py 2>/dev/null && echo "[OK] Proses dimatikan." || echo "[i] Tidak ada proses."
fi
command -v termux-wake-unlock >/dev/null 2>&1 && termux-wake-unlock
