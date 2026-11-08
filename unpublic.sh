#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
[ -f .tunnel.pid ] && kill "$(cat .tunnel.pid)" 2>/dev/null
pkill -f cloudflared 2>/dev/null; pkill -f _tunnel_loop 2>/dev/null
rm -f .tunnel.pid public_url.txt
echo "[OK] Tunnel dihentikan."
