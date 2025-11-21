import asyncio
from src.services.ollama.client import OllamaClient

async def test_ollama():
    client = OllamaClient()
    
    # Test 1: Health check
    health = await client.health_check()
    print("✅ Ollama is running:", health)
    
    # Test 2: Simple generation
    response = await client.generate("Say hello in one word")
    print("✅ LLM Response:", response)
    
    # Test 3: RAG-like query
    context = "Machine learning is a subset of AI."
    query = "What is machine learning?"
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
    
    response = await client.generate(prompt)
    print("✅ RAG Response:", response)

if __name__ == "__main__":
    asyncio.run(test_ollama())
