"""Provider-agnostic AI client for the Python ML API.

Env:
  AI_PROVIDER = ollama | openai | anthropic | venice | groq | openrouter
  AI_BASE_URL = optional override (default = provider's base URL)
  AI_MODEL    = model name
  AI_API_KEY  = required for cloud providers
"""
from __future__ import annotations
import os
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

PROVIDERS = {
    "ollama":     ("http://localhost:11434/v1",                "llama3.1:8b"),
    "openai":     ("https://api.openai.com/v1",                "gpt-4o-mini"),
    "anthropic":  ("https://api.anthropic.com/v1",             "claude-3-5-sonnet-20241022"),
    "venice":     ("https://api.venice.ai/v1",                 "llama-3.1-405b"),
    "groq":       ("https://api.groq.com/openai/v1",           "llama-3.1-70b-versatile"),
    "openrouter": ("https://openrouter.ai/api/v1",             "meta-llama/llama-3.1-70b-instruct"),
}

def get_provider() -> str:
    return os.environ.get("AI_PROVIDER", "ollama")

def get_base_url() -> str:
    return os.environ.get("AI_BASE_URL") or PROVIDERS[get_provider()][0]

def get_model() -> str:
    return os.environ.get("AI_MODEL") or PROVIDERS[get_provider()][1]

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
async def chat(prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
    provider = get_provider()
    api_key = os.environ.get("AI_API_KEY", "ollama")
    url = f"{get_base_url()}/chat/completions"
    payload = {
        "model": get_model(),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, json=payload, headers={"authorization": f"Bearer {api_key}"})
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
