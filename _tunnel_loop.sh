#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
while true; do
  ./cloudflared tunnel --url http://localhost:8888 --no-autoupdate > tunnel.log 2>&1 &
  T=$!
  for i in $(seq 1 40); do
    U=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' tunnel.log | head -1)
    [ -n "$U" ] && echo "$U" > public_url.txt && break
    sleep 1
  done
  wait $T
  sleep 4
done
