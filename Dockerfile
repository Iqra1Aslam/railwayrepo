FROM ollama/ollama:latest

COPY start.sh /start.sh
RUN chmod +x /start.sh
RUN pip install fastapi "uvicorn[standard]" httpx


# Don’t set ENV here — use Railway variable instead
# ENV OLLAMA_HOST=0.0.0.0:${PORT}

# Override the entrypoint so our script runs
ENTRYPOINT ["/bin/bash", "/start.sh"]
