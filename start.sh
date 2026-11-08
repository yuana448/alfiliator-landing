#!/usr/bin/env bash
# Launcher persisten: detached + wake-lock, aman dari penutupan sesi
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"; cd "$DIR" || exit 1
export PORT="${PORT:-8888}"
PIDF="$DIR/.server.pid"; LOG="$DIR/server.log"

if [ -f "$PIDF" ] && kill -0 "$(cat "$PIDF" 2>/dev/null)" 2>/dev/null; then
  echo "[=] Sudah jalan (PID $(cat "$PIDF")) -> http://localhost:$PORT"; exit 0
fi

command -v termux-wake-lock >/dev/null 2>&1 && termux-wake-lock && echo "[+] Wake-lock aktif."

if command -v setsid >/dev/null 2>&1; then
  nohup setsid python app.py >"$LOG" 2>&1 &
else
  nohup python app.py >"$LOG" 2>&1 &
fi
echo $! > "$PIDF"; disown 2>/dev/null || true; sleep 1

if kill -0 "$(cat "$PIDF")" 2>/dev/null; then
  echo "[OK] Node jalan di background (PID $(cat "$PIDF"))."
  echo "     Buka: http://localhost:$PORT   |   Log: $LOG"
else
  echo "[X] Gagal start."; tail -n 20 "$LOG"
fi
