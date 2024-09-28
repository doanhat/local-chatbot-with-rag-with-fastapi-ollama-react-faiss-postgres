import os  # Import os module

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost/chatbot_db"
)  # Read from environment variable
OLLAMA_API_BASE = os.getenv(
    "OLLAMA_API_BASE", "http://host.docker.internal:11434"
)  # Read from environment variable
FRONTEND_URL = os.getenv(
    "FRONTEND_URL", "http://localhost:3000"
)  # Read from environment variable
