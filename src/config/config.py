from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    postgres_database_url: str = "postgresql://user:pass@localhost:5432/db"
    
    # OpenSearch
    opensearch_host: str = "http://localhost:9200"
    
    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    
    # Redis
    redis_host: str = "localhost"
    
    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()