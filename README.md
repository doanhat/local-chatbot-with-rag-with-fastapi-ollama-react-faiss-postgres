# Local Chatbot with RAG

This project implements a local chatbot using Retrieval-Augmented Generation (RAG) technology. It consists of three main components: a chatbot API, a user interface, and the infrastructure to support the chatbot system.

Ideal for developers, researchers looking to implement a customizable, privacy-focused chatbot solution with the power of large language models and the flexibility of local deployment.

## Table of Contents

- [Chatbot API](#chatbot-api)
- [Chatbot UI](#chatbot-ui)
- [Chatbot Infrastructure](#chatbot-infrastructure)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

## Chatbot API

The chatbot-api component is responsible for handling the core logic of the chatbot, including:

- Processing user inputs
- Generating appropriate responses using RAG technology
- Managing conversation context
- Integrating with external services and databases

### Key Features

- RESTful API endpoints for chatbot interactions
- Document upload and text extraction (PDF, DOCX, TXT)
- Vector-based document search
- Integration with Ollama for language model inference
- Database storage for chat history and documents

### Technologies Used

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic for database migrations
- FAISS for vector storage
- Sentence Transformers for text embedding

## Chatbot UI

The chatbot-ui component provides the user interface for interacting with the chatbot. It includes:

- A responsive web interface built with React.js
- Real-time chat functionality
- Model selection from available models
- Document upload functionality
- Chat history display
- Dark mode UI using Material-UI

### Technologies Used

- React.js
- Material-UI
- Axios for API communication

## Chatbot Infrastructure

The chatbot-infrastructure component manages the deployment, scaling, and monitoring of the chatbot system. It includes:

- Containerization using Docker
- Docker Compose for local development and testing
- PostgreSQL database setup
- Environment configuration for API and UI components

### Key Components

- Docker containers for API, UI, and database
- Makefile for easy management of services
- Integration with locally running Ollama instance

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/doanhat/local-chatbot-with-rag.git
   cd local-chatbot-with-rag
   ```

2. Set up and start the infrastructure:
   ```bash
   cd chatbot-infrastructure
   make run
   ```

3. Access the components:
   - API: http://localhost:8000/api
   - UI: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

For detailed setup instructions for each component, refer to their individual README files:
- [Chatbot API README](chatbot-api/README.md)
- [Chatbot UI README](chatbot-ui/README.md)
- [Chatbot Infrastructure README](chatbot-infrastructure/README.md)
