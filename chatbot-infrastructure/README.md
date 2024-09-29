# Chatbot Infrastructure

This repository contains the infrastructure setup for a chatbot application using Docker. It includes services for a PostgreSQL database, an API, and a frontend application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Makefile Commands](#makefile-commands)
- [Checking Ollama Logs](#checking-ollama-logs)
- [License](#license)

## Prerequisites

- Docker Desktop installed on your machine (for macOS or Windows).
- Ollama installed on your local machine (for running the language model).
- Basic knowledge of Docker and Makefile usage.

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/doanhat/local-chatbot-with-rag-with-fastapi-ollama-react-faiss-postgres.git
   cd chatbot-infrastructure
   ```

2. **Set up environment variables**:
   Ensure that the `OLLAMA_API_BASE` in the `docker-compose.yml` file points to the correct URL for your locally running Ollama instance:
   ```yaml
   OLLAMA_API_BASE: http://host.docker.internal:11434
   ```

3. **Start the services**:
   Use the Makefile to start the services:
   ```bash
   make run
   ```

## Usage

- The API will be accessible at `http://localhost:8000/api`.
- The frontend application will be accessible at `http://localhost:3000`.

## Makefile Commands

The following commands are available in the Makefile:

- `make run`: Checks if Ollama is running; if not, it starts Ollama and then launches Docker Compose.
- `make stop`: Stops the Docker Compose services but leaves Ollama running.
- `make stop-all`: Stops both Docker Compose services and the Ollama process.
- `make clean`: Stops all services and removes Docker volumes.
- `make ollama-logs`: Displays the logs for the Ollama process.


