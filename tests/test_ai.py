import os
from ml_api.ai import get_provider, get_base_url, get_model

def test_default_provider_is_known():
    for p in ["ollama", "openai", "anthropic", "venice", "groq", "openrouter"]:
        os.environ["AI_PROVIDER"] = p
        assert get_provider() == p
        assert get_base_url().startswith("http")
        assert get_model()

def test_overrides_take_effect():
    os.environ["AI_PROVIDER"] = "ollama"
    os.environ["AI_BASE_URL"] = "http://example.test/v1"
    os.environ["AI_MODEL"] = "test-model"
    assert get_base_url() == "http://example.test/v1"
    assert get_model() == "test-model"
