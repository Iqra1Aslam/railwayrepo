FROM ollama/ollama:latest
# Optional: nothing else needed; we’ll use an entrypoint script to pre-pull
COPY start.sh /start.sh
RUN chmod +x /start.sh
ENV OLLAMA_HOST=0.0.0.0:${PORT}
VOLUME ["/root/.ollama"]
CMD ["/start.sh"]
