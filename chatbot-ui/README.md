# Chatbot UI

This is the frontend application for the Local Chatbot with RAG project. It provides a user interface for interacting with the chatbot, uploading documents, and viewing chat history.

## Features

- Chat interface for interacting with the AI model
- Model selection from available models
- Document upload functionality
- Chat history display
- Dark mode UI using Material-UI


## Prerequisites

- Node.js (version 16 or later)
- npm (usually comes with Node.js)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/doanhat/local-chatbot-with-rag-with-fastapi-ollama-react-faiss-postgres.git
   cd local-chatbot-with-rag-with-fastapi-ollama-react-faiss-postgres/chatbot-ui
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a `.env` file in the root of the `chatbot-ui` directory and add:
   ```
   REACT_APP_API_BASE_URL=http://localhost:8000/api
   ```
   Adjust the URL if your backend is running on a different host or port.

## Running the Application

To start the development server:
```bash
npm start
```


The application will be available at `http://localhost:3000`.

## Building for Production

To create a production build:
```bash
npm run build
```
This will create a `build` directory with the compiled assets.

## Docker Support

A Dockerfile is provided for containerization. To build and run the Docker image:
```bash
docker build -t chatbot-ui .
docker run -p 3000:3000 chatbot-ui
```

This will start the application in a Docker container, accessible at `http://localhost:3000`.


## API Integration

The application communicates with the backend API using axios. The API calls are centralized in `src/services/api.js`. Make sure the backend server is running and accessible.

## Components

- `Chat.js`: Handles the chat interface and message exchange.
- `ChatHistory.js`: Displays the chat history.
- `DocumentUpload.js`: Provides functionality to upload documents.
- `ModelSelector.js`: Allows selection of different AI models.

## Styling

The application uses Material-UI for styling and components. A dark theme is applied by default.

## Environment Variables

- `REACT_APP_API_BASE_URL`: The base URL for the backend API.