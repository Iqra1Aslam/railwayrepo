from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

# Use environment variable or fallback
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

app = FastAPI(title="Ollama Wrapper", version="1.0")

# Request schema
class GenerateRequest(BaseModel):
    prompt: str
    model: str = "deepseek-r1:1.5b"
    stream: bool | None = False
    options: dict | None = None

# Response schema
class GenerateResponse(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"status": "ok", "message": "Ollama wrapper running"}

@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    """
    Call Ollama API running inside container to generate text.
    """
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": req.model,
                    "prompt": req.prompt,
                    "stream": req.stream,
                    "options": req.options or {},
                },
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ollama error: {response.text}",
                )

            data = response.json()
            # Ollama’s /api/generate returns {"response": "..."} not "text"
            return {"text": data.get("response", "")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error contacting Ollama: {str(e)}")
