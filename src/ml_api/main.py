"""FastAPI app with a /health endpoint and a /chat that delegates to any AI provider."""
from __future__ import annotations
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .ai import chat, get_provider, get_model

@asynccontextmanager
async def lifespan(_: FastAPI):
    print(f"starting up with provider={get_provider()} model={get_model()}")
    yield

app = FastAPI(title="template-python-ml-api", version="0.1.0", lifespan=lifespan)

class Health(BaseModel):
    status: str = "ok"
    service: str = "template-python-ml-api"
    version: str = "0.1.0"
    provider: str
    model: str

class ChatIn(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=8000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1, le=8192)

class ChatOut(BaseModel):
    content: str
    provider: str
    model: str

@app.get("/health", response_model=Health)
async def health() -> Health:
    return Health(provider=get_provider(), model=get_model())

@app.post("/chat", response_model=ChatOut)
async def chat_endpoint(body: ChatIn) -> ChatOut:
    try:
        content = await chat(body.prompt, temperature=body.temperature, max_tokens=body.max_tokens)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"upstream: {e}")
    return ChatOut(content=content, provider=get_provider(), model=get_model())
