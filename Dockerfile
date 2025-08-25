FROM ollama/ollama:latest

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install FastAPI + Uvicorn
RUN pip3 install fastapi uvicorn

COPY start.sh /start.sh
RUN chmod +x /start.sh

# Entrypoint
ENTRYPOINT ["/bin/bash", "/start.sh"]
