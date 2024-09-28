from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config.env import FRONTEND_URL
from api.routers import chat, documents, llm


def create_app():
    app = FastAPI(
        title="Chatbot API",
        version="1.0.0",
        description="This API allows you to interact with the chatbot and manage chat history.",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(chat.router, prefix="/api", tags=["chat"])
    app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
    app.include_router(llm.router, prefix="/api/models", tags=["models"])

    @app.get("/")
    async def root() -> dict[str, str]:
        return {"message": "Welcome to the Chatbot API"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    from api.database import Base, engine

    # Create database tables
    Base.metadata.create_all(bind=engine)

    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
