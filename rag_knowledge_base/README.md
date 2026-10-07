# RAG Knowledge Base API

A FastAPI-based Retrieval-Augmented Generation (RAG) backend that supports PDF ingestion, semantic retrieval, grounded answer generation, source citation, and basic retrieval evaluation.

## Features

- Upload PDF documents through a FastAPI endpoint
- Extract and clean text from PDFs
- Split documents into overlapping chunks
- Generate embeddings with OpenAI
- Store vectors and metadata in ChromaDB
- Retrieve Top-K relevant chunks using semantic search
- Generate grounded answers using an LLM
- Return structured source citations
- Evaluate retrieval quality with Hit@1 and Hit@3

## Architecture

```text
PDF Upload
   ↓
FastAPI Router
   ↓
Ingestion Service
   ↓
PDF Parsing
   ↓
Chunking
   ↓
Embedding
   ↓
ChromaDB
   ↓
Retrieval Service
   ↓
RAG Service
   ↓
LLM
   ↓
Answer + Sources
```

## Project Structure

```text
rag_knowledge_base/
├── app/
│   ├── main.py
│   ├── routers/
│   │   ├── documents.py
│   │   └── ask.py
│   ├── services/
│   │   ├── ingestion_service.py
│   │   ├── retrieval_service.py
│   │   └── rag_service.py
│   └── schemas/
│       └── rag.py
├── evaluation/
│   ├── __init__.py
│   ├── evaluation_cases.py
│   └── evaluate_retrieval.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Tech Stack

- Python
- FastAPI
- OpenAI API
- ChromaDB
- PyPDF
- Pydantic
- Uvicorn

## Setup

Create and activate a Python virtual environment.

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Do not commit the `.env` file or expose your API key.

## Run the API

From the project root:

```bash
python -m uvicorn app.main:app --reload
```

If port 8000 is unavailable:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

or:

```text
http://127.0.0.1:8001/docs
```

## API Endpoints

### Upload Document

```http
POST /documents/upload
```

Uploads a PDF document, extracts its content, splits the text into chunks, generates embeddings, and stores the chunks and metadata in ChromaDB.

Example response:

```json
{
  "filename": "vector_store.pdf",
  "chunk_count": 6,
  "stored_chunks": 18
}
```

### Ask a Question

```http
POST /ask
```

Example request:

```json
{
  "question": "Why is chunk overlap useful?"
}
```

Example response:

```json
{
  "question": "Why is chunk overlap useful?",
  "answer": "Chunk overlap helps preserve context across chunk boundaries.",
  "sources": [
    {
      "source": "chunking.pdf",
      "page": 2
    }
  ]
}
```

## RAG Pipeline

The application follows the following workflow:

```text
Document Upload
    ↓
PDF Parsing
    ↓
Text Cleaning
    ↓
Chunking with Overlap
    ↓
Embedding Generation
    ↓
ChromaDB Storage
    ↓
User Question
    ↓
Query Embedding
    ↓
Top-K Semantic Retrieval
    ↓
Context Construction
    ↓
Grounded LLM Generation
    ↓
Answer + Structured Sources
```

## Retrieval Evaluation

The project includes a small curated retrieval evaluation set containing 8 queries.

The current evaluation uses:

- Hit@1
- Hit@3

Current result:

```text
Hit@1: 1.0
Hit@3: 1.0
```

On this small curated 8-query evaluation set, the retriever achieved 100% Hit@1 and Hit@3.

This result should not be interpreted as general retrieval accuracy because the evaluation dataset is small and manually constructed.

The evaluation script reuses the same retrieval service used by the API, ensuring that the evaluation reflects the actual retrieval logic of the application.

Run the evaluation from the project root:

```bash
python -m evaluation.evaluate_retrieval
```

## Project Design

The project separates HTTP routing, business logic, data schemas, and retrieval logic into different modules.

```text
routers/
    Handles HTTP requests and responses

services/
    Contains ingestion, retrieval, and RAG business logic

schemas/
    Defines request and response data structures

evaluation/
    Contains retrieval evaluation cases and metrics
```

This structure makes the project easier to maintain, test, and extend.

## Current Limitations

The current version is a V1 implementation and still has several limitations:

- Uses fixed-size word-based chunking
- Uses dense vector retrieval only
- Uses a small manually constructed evaluation dataset
- No reranking
- No hybrid keyword and semantic retrieval
- No query rewriting
- Limited production-grade error handling
- No authentication or authorization
- No Redis caching
- No tracing or observability
- No deployment configuration yet

## Future Improvements

Planned improvements include:

- Query rewriting
- Hybrid search
- Reranking
- Metadata filtering
- Improved chunking strategies
- Larger retrieval evaluation datasets
- Answer quality evaluation
- Redis caching
- Async processing
- Retry and fallback mechanisms
- Rate limiting
- Logging and tracing
- Observability
- Docker deployment
- Agent integration

## Version

Current version:

```text
RAG Knowledge Base V1
```