#!/usr/bin/env bash
set -euo pipefail

# Start Ollama in the background
ollama serve &
OLLAMA_PID=$!

# Give Ollama time to start
echo "Starting Ollama..."
sleep 5

# Pull your model (optional, will be cached after first time)
ollama pull deepseek-r1:1.5b || true

# Start FastAPI (using uvicorn to serve main.py)
echo "Starting FastAPI app..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Wait on both processes
wait -n
