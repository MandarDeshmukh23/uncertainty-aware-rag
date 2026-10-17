# Uncertainty-Aware Distributed RAG

A production-grade, distributed Retrieval-Augmented Generation (RAG) backend. This system decouples document ingestion from HTTP request handling using message queues, and implements mathematical guardrails using token log-probabilities to mitigate LLM hallucinations.

## System Architecture
1. **API Gateway (FastAPI):** Handles non-blocking HTTP requests and Pydantic validation.
2. **Metadata Store (SQLite/SQLAlchemy):** Tracks document processing state.
3. **Message Broker (RabbitMQ):** Buffers incoming ingestion jobs to prevent server overload.
4. **Background Workers (Celery):** Executes heavy ML pipelines (text extraction, chunking, embedding) asynchronously.
5. **Vector Store (Qdrant):** Stores 384-dimensional embeddings for cosine-similarity semantic retrieval.
6. **LLM Engine (Ollama / Llama 3.2):** Generates answers and calculates stochastic generative uncertainty based on output logprobs.

## Core Features
* **Asynchronous Processing:** Large PDFs are processed in the background without blocking the main API thread.
* **Semantic Search:** Text chunks are embedded using `all-MiniLM-L6-v2` for high-speed spatial retrieval.
* **Hallucination Mitigation:** The generation service evaluates vector distance and token entropy, explicitly refusing to answer if the confidence score drops below 0.85.

## Local Development Setup
1. Boot infrastructure: `docker run -d -p 5672:5672 rabbitmq:3-management` and `docker run -d -p 6333:6333 qdrant/qdrant`
2. Start local LLM: `ollama run llama3.2:1b`
3. Start the API: `uvicorn src.api.main:app --reload`
4. Start the Worker: `celery -A src.workers.celery_app worker --loglevel=info -P solo`