# template-python-ml-api

A FastAPI + Pydantic v2 + AI-provider-agnostic Python template, with CI
delegated to [muffy86/infra-automation](https://github.com/muffy86/infra-automation).

## Quick start

```bash
uv sync
cp .env.example .env
uv run uvicorn ml_api.main:app --reload
curl http://localhost:8000/health
```

## Endpoints

- `GET /health` — service + provider + model
- `POST /chat` — body `{"prompt": "...", "temperature": 0.7, "max_tokens": 1024}`

## What's wired up

- `pyproject.toml` — uv-managed, ruff, mypy, pytest-asyncio
- `src/ml_api/main.py` — FastAPI app with `/health` and `/chat`
- `src/ml_api/ai.py` — provider-agnostic AI client with retries
- `tests/test_health.py` + `tests/test_ai.py` — smoke tests
- CI delegates to `muffy86/infra-automation/.github/workflows/ci-python.yml@main`
