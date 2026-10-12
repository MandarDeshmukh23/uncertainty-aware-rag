# Uncertainty-Aware Distributed RAG

A production-grade, distributed Retrieval-Augmented Generation (RAG) platform with probabilistic uncertainty calibration, asynchronous document ingestion, and decoupled microservices.

## Architecture Overview
- **API Gateway**: FastAPI service managing query endpoints and ingestion triggers.
- **Message Broker**: RabbitMQ managing asynchronous chunking and embedding pipelines.
- **Worker Node**: Background worker ingesting, vectorizing, and populating vector stores.
- **Inference & Uncertainty Engine**: Evaluates vector similarity confidence intervals and LLM logprob calibration before response generation.