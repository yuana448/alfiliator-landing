#!/usr/bin/env bash
set -u
cd "$(dirname "$0")" || exit 1
if [ -f .tunnel.pid ] && kill -0 "$(cat .tunnel.pid 2>/dev/null)" 2>/dev/null; then
  echo "[=] Sudah jalan: $(cat public_url.txt 2>/dev/null)"; exit 0
fi
command -v termux-wake-lock >/dev/null 2>&1 && termux-wake-lock
bash ./start.sh
if [ ! -x ./cloudflared ]; then
  case "$(uname -m)" in aarch64|arm64) A=arm64;; armv7l|armv8l) A=arm;; x86_64) A=amd64;; *) A=arm64;; esac
  echo "[i] Mengunduh cloudflared ($A)..."
  curl -fsSL -o cloudflared "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-$A" || { echo "[X] unduh gagal"; exit 1; }
  chmod +x cloudflared
fi
nohup setsid bash ./_tunnel_loop.sh >/dev/null 2>&1 &
echo $! > .tunnel.pid
disown 2>/dev/null || true
for i in $(seq 1 45); do [ -s public_url.txt ] && break; sleep 1; done
[ -s public_url.txt ] && echo "[OK] Publik: $(cat public_url.txt)" || { echo "[X] gagal, cek tunnel.log"; tail -n 12 tunnel.log; }
