from src.config import get_settings

def test_settings():
    settings = get_settings()
    assert settings.ollama_host == "http://localhost:11434"
    assert settings.ollama_model == "llama3"
