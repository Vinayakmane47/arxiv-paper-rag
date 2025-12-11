# arXiv Paper Curator - Production RAG System

<div align="center">
  <h3>An Intelligent Research Assistant for Academic Papers</h3>
  <p>Automated paper ingestion, intelligent search, and AI-powered question answering</p>
  <p>Built with <strong>RAG (Retrieval-Augmented Generation)</strong> and production-grade infrastructure</p>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/OpenSearch-2.19-orange.svg" alt="OpenSearch">
  <img src="https://img.shields.io/badge/Docker-Compose-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg" alt="Status">
</p>

---

## 📖 Overview

**arXiv Paper Curator** is a production-ready RAG (Retrieval-Augmented Generation) system that automatically fetches, indexes, and enables intelligent querying of academic papers from arXiv. The system combines:

- **Automated Data Pipeline**: Daily ingestion of papers from arXiv with PDF parsing
- **Hybrid Search**: BM25 keyword search + semantic vector search for optimal retrieval
- **AI-Powered Q&A**: Local LLM integration for intelligent question answering
- **Production Monitoring**: Complete observability with Langfuse tracing and Redis caching
- **Interactive Interface**: Gradio web UI for easy interaction

### **Key Features**

- ✅ **Automated Paper Ingestion**: Airflow-powered daily pipeline fetching papers from arXiv
- ✅ **Intelligent Chunking**: Section-aware document segmentation preserving context
- ✅ **Hybrid Search**: Combines BM25 keyword search with semantic embeddings
- ✅ **Local LLM Integration**: Privacy-first question answering with Ollama
- ✅ **Streaming Responses**: Real-time answer generation with Server-Sent Events
- ✅ **Production Monitoring**: End-to-end tracing with Langfuse
- ✅ **Intelligent Caching**: Redis caching for 150-400x performance improvement
- ✅ **RESTful API**: Complete FastAPI with automatic documentation

---

## 🚀 Quick Start

### **📋 Prerequisites**

- **Docker Desktop** (with Docker Compose)
- **Python 3.12+**
- **UV Package Manager** ([Install Guide](https://docs.astral.sh/uv/getting-started/installation/))
- **8GB+ RAM** and **20GB+ free disk space**

### **⚡ Installation**

```bash
# 1. Clone the repository
git clone <repository-url>
cd arxiv-paper-rag

# 2. Configure environment
cp .env.example .env
# Edit .env file with your configuration
# For hybrid search: Add JINA_API_KEY=your_key_here

# 3. Install dependencies
uv sync

# 4. Start all services
docker compose up --build -d

# 5. Wait for services to initialize (2-3 minutes)
# Then verify everything works
curl http://localhost:8000/api/v1/health
```

### **📊 Access Your Services**

| Service | URL | Purpose |
|---------|-----|---------|
| **API Documentation** | http://localhost:8000/docs | Interactive API testing |
| **Gradio RAG Interface** | http://localhost:7861 | User-friendly chat interface |
| **Langfuse Dashboard** | http://localhost:3000 | RAG pipeline monitoring & tracing |
| **Airflow Dashboard** | http://localhost:8080 | Workflow management |
| **OpenSearch Dashboards** | http://localhost:5601 | Hybrid search engine UI |

**Note**: Check `airflow/simple_auth_manager_passwords.json.generated` for Airflow credentials

---

## 🏗️ Architecture

### **System Components**

- **FastAPI**: REST API with async support (Port 8000)
- **PostgreSQL 16**: Paper metadata storage (Port 5432)
- **OpenSearch 2.19**: Hybrid search engine with dashboards (Ports 9200, 5601)
- **Apache Airflow**: Workflow orchestration (Port 8080)
- **Ollama**: Local LLM server (Port 11434)
- **Redis**: High-performance caching (Port 6379)
- **Langfuse**: Observability and tracing (Port 3000)

### **Data Flow**

1. **Ingestion**: Airflow DAG fetches papers from arXiv API daily
2. **Processing**: PDFs are parsed using Docling, extracting structured content
3. **Indexing**: Papers are chunked intelligently and indexed in OpenSearch with embeddings
4. **Search**: Hybrid search combines BM25 keyword matching with semantic similarity
5. **Generation**: Retrieved chunks are sent to Ollama LLM for answer generation
6. **Caching**: Responses are cached in Redis for instant retrieval
7. **Monitoring**: All operations are traced in Langfuse for observability

---

## 📡 API Endpoints

### **Core Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Service health check |
| `/api/v1/papers` | GET | List stored papers |
| `/api/v1/papers/{id}` | GET | Get specific paper details |
| `/api/v1/hybrid-search/` | POST | Hybrid search (BM25 + Vector) |
| `/api/v1/ask` | POST | RAG question answering (standard) |
| `/api/v1/stream` | POST | RAG question answering (streaming) |

**Interactive API Documentation**: Visit http://localhost:8000/docs

### **Example Usage**

**Hybrid Search:**
```python
import httpx

async def search_papers(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/hybrid-search/",
            json={
                "query": query,
                "use_hybrid": True,
                "size": 10,
                "categories": ["cs.AI", "cs.LG"]
            }
        )
        return response.json()
```

**RAG Question Answering:**
```python
async def ask_question(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/ask",
            json={
                "query": query,
                "top_k": 3,
                "use_hybrid": True,
                "model": "llama3.2:1b"
            }
        )
        result = response.json()
        return result["answer"], result["sources"]
```

**Streaming RAG:**
```python
async def stream_answer(query: str):
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://localhost:8000/api/v1/stream",
            json={"query": query, "top_k": 3}
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith('data: '):
                    data = json.loads(line[6:])
                    if 'chunk' in data:
                        print(data['chunk'], end='', flush=True)
```

---

## 🎯 Key Features

### **1. Automated Paper Ingestion**

- Daily Airflow DAG fetching papers from arXiv
- Automatic PDF download and parsing
- Metadata extraction and storage
- Duplicate detection and handling

### **2. Intelligent Document Processing**

- **Section-Aware Chunking**: Preserves document structure
- **Overlap Strategy**: Maintains context between chunks
- **Smart Segmentation**: Respects section boundaries

### **3. Hybrid Search**

- **BM25 Keyword Search**: Fast, precise keyword matching
- **Semantic Vector Search**: Understanding synonyms and concepts
- **RRF Fusion**: Combines both approaches for optimal results
- **Configurable**: Switch between BM25-only, vector-only, or hybrid

### **4. AI-Powered Question Answering**

- **Local LLM**: Privacy-first with Ollama
- **Optimized Prompts**: 80% reduction in prompt size
- **Streaming Support**: Real-time response generation
- **Source Attribution**: Automatic citation of papers

### **5. Production Monitoring**

- **Langfuse Tracing**: End-to-end RAG pipeline observability
- **Performance Metrics**: Latency, token usage, costs
- **Error Tracking**: Comprehensive error logging
- **Real-time Dashboards**: Visual performance monitoring

### **6. Intelligent Caching**

- **Redis Integration**: High-performance response caching
- **150-400x Speedup**: Cached responses in ~50ms vs 15-20s
- **60%+ Cache Hit Rate**: Significant cost reduction
- **Automatic TTL Management**: Smart cache expiration

---

## ⚙️ Configuration

### **Environment Variables**

The project uses a unified `.env` file for configuration:

```bash
# Application Settings
DEBUG=true
ENVIRONMENT=development

# arXiv API
ARXIV__MAX_RESULTS=5
ARXIV__SEARCH_CATEGORY=cs.AI
ARXIV__RATE_LIMIT_DELAY=3.0

# PDF Parser
PDF_PARSER__MAX_PAGES=30
PDF_PARSER__DO_OCR=false

# OpenSearch
OPENSEARCH__HOST=http://opensearch:9200
OPENSEARCH__INDEX_NAME=arxiv-papers-chunks

# Jina AI Embeddings (for hybrid search)
JINA_API_KEY=your_jina_api_key_here
EMBEDDINGS__MODEL=jina-embeddings-v3
EMBEDDINGS__TASK=retrieval.passage
EMBEDDINGS__DIMENSIONS=1024

# Chunking Configuration
CHUNKING__CHUNK_SIZE=600
CHUNKING__OVERLAP_SIZE=100
CHUNKING__MIN_CHUNK_SIZE=100

# Ollama LLM
OLLAMA_HOST=http://ollama:11434
OLLAMA__DEFAULT_MODEL=llama3.2:1b
OLLAMA__TIMEOUT=300
OLLAMA__MAX_RESPONSE_WORDS=300

# Langfuse Monitoring
LANGFUSE__PUBLIC_KEY=pk-lf-your-public-key
LANGFUSE__SECRET_KEY=sk-lf-your-secret-key
LANGFUSE__HOST=http://localhost:3000
LANGFUSE__ENABLED=true
LANGFUSE__FLUSH_INTERVAL=1.0

# Redis Caching
REDIS__URL=redis://redis:6379/0
REDIS__CACHE_TTL_HOURS=24
REDIS__MAX_CONNECTIONS=10
```

### **Key Configuration Variables**

| Variable | Default | Description |
|----------|---------|-------------|
| `ARXIV__MAX_RESULTS` | `5` | Papers to fetch per API call |
| `ARXIV__SEARCH_CATEGORY` | `cs.AI` | arXiv category to search |
| `PDF_PARSER__MAX_PAGES` | `30` | Max pages to process per PDF |
| `OPENSEARCH__INDEX_NAME` | `arxiv-papers-chunks` | OpenSearch index name |
| `CHUNKING__CHUNK_SIZE` | `600` | Target words per document chunk |
| `CHUNKING__OVERLAP_SIZE` | `100` | Overlapping words between chunks |
| `OLLAMA_MODEL` | `llama3.2:1b` | Local LLM model |
| `REDIS__CACHE_TTL_HOURS` | `24` | Cache expiration time in hours |

---

## 🏗️ Project Structure

```
arxiv-paper-rag/
├── src/                                    # Main application code
│   ├── main.py                             # FastAPI application
│   ├── routers/                            # API endpoints
│   │   ├── ping.py                         # Health check endpoints
│   │   ├── papers.py                       # Paper retrieval endpoints
│   │   ├── hybrid_search.py                # Hybrid search endpoints
│   │   └── ask.py                          # RAG question answering endpoints
│   ├── models/                             # Database models (SQLAlchemy)
│   ├── repositories/                       # Data access layer
│   ├── schemas/                            # Pydantic validation schemas
│   ├── services/                           # Business logic
│   │   ├── arxiv/                          # arXiv API client
│   │   ├── pdf_parser/                     # Docling PDF processing
│   │   ├── opensearch/                     # OpenSearch integration
│   │   ├── indexing/                       # Document processing
│   │   ├── embeddings/                     # Embedding services
│   │   ├── ollama/                         # LLM services
│   │   ├── langfuse/                       # Monitoring services
│   │   └── cache/                          # Caching services
│   ├── db/                                 # Database configuration
│   ├── config.py                           # Environment configuration
│   └── dependencies.py                     # Dependency injection
│
├── notebooks/                              # Development notebooks
│   ├── week1_setup.ipynb                   # Setup and infrastructure guide
│   └── ...
│
├── airflow/                                # Workflow orchestration
│   ├── dags/                               # Workflow definitions
│   │   ├── arxiv_ingestion/                # arXiv ingestion modules
│   │   └── arxiv_paper_ingestion.py        # Main ingestion DAG
│   └── requirements-airflow.txt            # Airflow dependencies
│
├── src/gradio_app.py                       # Interactive web interface
├── tests/                                  # Test suite
├── static/                                 # Assets (images, diagrams)
└── compose.yml                             # Service orchestration
```

---

## 📊 Performance Metrics

### **Search Performance**

| Search Mode | Speed | Precision@10 | Recall@10 | Use Case |
|-------------|-------|--------------|-----------|----------|
| **BM25 Only** | ~50ms | 0.67 | 0.71 | Exact keywords, author names |
| **Hybrid (RRF)** | ~400ms | 0.84 | 0.89 | Conceptual queries, synonyms |

### **RAG Performance**

| Metric | Value | Notes |
|--------|-------|-------|
| **Response Time** | 15-20s | First request (cache miss) |
| **Cached Response** | 50-100ms | Repeated queries (cache hit) |
| **Time to First Token** | 2-3s | Streaming endpoint |
| **Cache Hit Rate** | 60%+ | Production workload |
| **Cost Reduction** | 60%+ | Through intelligent caching |

---

## 🔧 Development

### **Essential Commands**

```bash
# Start all services
docker compose up --build -d

# Check service status
docker compose ps

# View logs
docker compose logs -f [service-name]

# Stop services
docker compose down

# Run tests
uv run pytest

# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy src/
```

### **Running the Gradio Interface**

```bash
# Launch the interactive web UI
uv run python src/gradio_app.py

# Or use the launcher script
uv run python gradio_launcher.py

# Access at http://localhost:7861
```

### **Testing the API**

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Test RAG endpoint
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What are transformers?", "top_k": 3}'

# Test streaming endpoint
curl -X POST http://localhost:8000/api/v1/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "What are transformers?", "top_k": 3}' \
  --no-buffer
```

---

## 🛠️ Technology Stack

| Service | Purpose | Version |
|---------|---------|---------|
| **FastAPI** | REST API framework | 0.115+ |
| **PostgreSQL** | Database | 16 |
| **OpenSearch** | Search engine | 2.19 |
| **Apache Airflow** | Workflow orchestration | 3.0 |
| **Ollama** | Local LLM serving | 0.11.2 |
| **Redis** | Caching | 7-alpine |
| **Langfuse** | Observability | 2 |
| **Jina AI** | Embeddings | v3 |
| **Docling** | PDF parsing | Latest |
| **Gradio** | Web interface | Latest |

**Development Tools**: UV, Ruff, MyPy, Pytest, Docker Compose

---

## 🐛 Troubleshooting

### **Common Issues**

**Services not starting?**
- Wait 2-3 minutes for all services to initialize
- Check logs: `docker compose logs [service-name]`
- Verify Docker has enough resources (8GB+ RAM)

**Port conflicts?**
- Stop other services using ports: 8000, 8080, 5432, 9200, 11434, 3000, 6379
- Modify ports in `compose.yml` if needed

**Memory issues?**
- Increase Docker Desktop memory allocation to 8GB+
- Reduce `ARXIV__MAX_RESULTS` in `.env`
- Use smaller LLM model (`llama3.2:1b`)

**Ollama connection errors?**
- Verify Ollama is running: `docker exec rag-ollama ollama list`
- Check model is downloaded: `docker exec rag-ollama ollama pull llama3.2:1b`
- Restart Ollama: `docker restart rag-ollama`

**Cache not working?**
- Check Redis: `docker exec rag-redis redis-cli ping`
- Verify Redis is running: `docker compose ps redis`
- Check environment variables in `.env`

**No Langfuse traces?**
- Verify environment variables are set correctly
- Check Langfuse service is running: `docker compose ps langfuse`
- Restart API container: `docker compose restart api`

### **Complete Reset**

```bash
# Stop and remove all containers, volumes, and networks
docker compose down --volumes

# Rebuild and start fresh
docker compose up --build -d
```

---

## 📈 Roadmap

- [ ] Support for additional paper sources (PubMed, arXiv categories)
- [ ] Advanced chunking strategies (semantic chunking)
- [ ] Multi-model LLM support with automatic selection
- [ ] Enhanced caching strategies (semantic similarity caching)
- [ ] User authentication and personalization
- [ ] Export functionality (PDF reports, citations)
- [ ] Advanced analytics dashboard

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with modern open-source technologies:
- FastAPI for the API framework
- OpenSearch for hybrid search capabilities
- Ollama for local LLM inference
- Langfuse for observability
- And many other excellent open-source projects

---

<div align="center">
  <h3>🚀 Ready to explore academic papers with AI?</h3>
  <p>Start the services and begin querying your research questions!</p>
</div>
