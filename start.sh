#!/usr/bin/env bash
set -euo pipefail
# Start Ollama, then pull your model once, then wait on the server
ollama serve & 
pid=$!
# tiny wait so the API is up (for cases where pull contacts local API)
sleep 5
ollama pull deepseek-r1:1.5b || true
wait "$pid"
