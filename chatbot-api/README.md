# Local Chatbot with RAG

This folder implements a local chatbot using Retrieval-Augmented Generation (RAG) technology. It consists of a FastAPI-based backend API that interacts with a language model, manages document storage, and provides chat functionality.


## Features

- Chat functionality with RAG-enhanced responses
- Document upload and text extraction (PDF, DOCX, TXT)
- Vector-based document search
- Integration with Ollama for language model inference
- Database storage for chat history and documents
- Alembic for database migrations

## Technologies Used

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- FAISS for vector storage
- Sentence Transformers for text embedding
- Ollama for language model integration
- Docker for containerization

## Getting Started

### Prerequisites

- Python 3.12
- Poetry for dependency management
- Docker (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/doanhat/local-chatbot-with-rag.git
   cd local-chatbot-with-rag/chatbot-api
   ```

2. Install dependencies:
   ```
   make install
   ```

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the API (Note: you need have ollama and postgres running on your local machine):
   ```bash
   uvicorn api.main:app --reload
   ```

### Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t chatbot-api .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 -e DATABASE_URL=your_db_url -e OLLAMA_API_BASE=your_ollama_url chatbot-api
   ```

## Usage

The API provides the following main endpoints:

- `/api/chat`: Send and receive chat messages
- `/api/documents/upload`: Upload documents
- `/api/documents/search`: Search for relevant documents
- `/api/models`: List available language models

For detailed API documentation, visit `http://localhost:8000/docs` after starting the server.

## Development

- Use `make check` to run linters and static analysis
- Use `make test` to run unit tests
- Use `make requirements.txt` to generate a requirements.txt file

