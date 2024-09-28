import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import (
    ChatHistory,
    ChatHistoryList,
    ChatHistoryResponse,
    ChatInput,
    ChatResponse,
    Document,
)
from api.services.ollama import generate_response
from api.services.vector_store import vector_store
from api.utils.text_processing import generate_embedding

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat(chat_input: ChatInput, db: Session = Depends(get_db)):
    logger.info("Chat endpoint called with message: %s", chat_input.message)

    try:
        query_embedding = generate_embedding(chat_input.message)
        logger.info("Embedding generated")

        search_results = vector_store.search(query_embedding, k=3)
        logger.info("Vector store search completed")

        document_ids = [doc_id for doc_id, _ in search_results]
        relevant_docs = db.query(Document).filter(Document.id.in_(document_ids)).all()
        logger.info("Retrieved %d relevant documents", len(relevant_docs))

        context = "\n\n".join(
            [
                f"Document: {doc.filename}\nContent: {doc.content[:500]}..."
                for doc in relevant_docs
            ]
        )
    except IndexError:
        # Handle the case when the vector store is empty
        context = "No relevant documents found."

    # Prepare the prompt with context
    prompt = f"Context:\n{context}\n\nUser: {chat_input.message}\nAssistant: Based on the context provided (if any), "

    # Generate response using Ollama
    response = await generate_response(chat_input.model, prompt)

    # Save chat history
    print("Adding chat history to the database...")
    chat_history = ChatHistory(
        user_input=chat_input.message,
        bot_response=response,
        model=chat_input.model,
    )
    db.add(chat_history)
    db.commit()

    return ChatResponse(message=response)


@router.get("/chat/history", response_model=ChatHistoryList)
def get_chat_history(db: Session = Depends(get_db)) -> ChatHistoryList:
    logger.debug("get_chat_history called")
    history = db.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).all()
    logger.debug(f"Retrieved {len(history)} chat history items")
    return ChatHistoryList(
        chat_history=[ChatHistoryResponse.model_validate(item) for item in history]
    )
