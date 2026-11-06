sed -i 's/bio_link\.py/app.py/g' start.sh stop.sh README.md .github/workflows/ci.yml 2>/dev/null
grep -rn "bio_link\.py\|app\.py" start.sh stop.sh README.md .github/workflows/ci.yml
