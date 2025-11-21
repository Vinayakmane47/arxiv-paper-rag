import httpx
from src.config import get_settings

class OllamaClient:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.ollama_host
        self.model = self.settings.ollama_model
    
    async def health_check(self) -> dict:
        """Check if Ollama is running."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/version")
            return response.json()
    
    async def generate(self, prompt: str) -> str:
        """Generate text from LLM."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json()["response"]