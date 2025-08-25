from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

# Your local Ollama server
OLLAMA_URL = "http://localhost:11434/api/chat"

app = FastAPI(title="Ollama OpenAI-Compatible API", version="1.0")

# Input schema (similar to OpenAI API)
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    stream: bool | None = False  # disable streaming by default
    options: dict | None = None  # extra Ollama params


@app.post("/v1/chat/completions")
async def create_chat_completion(req: ChatCompletionRequest):
    try:
        payload = {
            "model": req.model,
            "messages": [{"role": m.role, "content": m.content} for m in req.messages],
        }

        if req.options:
            payload["options"] = req.options

        async with httpx.AsyncClient() as client:
            r = await client.post(OLLAMA_URL, json=payload)
            r.raise_for_status()
            data = r.json()

        # Mimic OpenAI’s response format
        return {
            "id": "chatcmpl-12345",
            "object": "chat.completion",
            "model": req.model,
            "choices": [
                {
                    "index": 0,
                    "message": data["message"],
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"status": "ok", "message": "Ollama proxy is running"}
