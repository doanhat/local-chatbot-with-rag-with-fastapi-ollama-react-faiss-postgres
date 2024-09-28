import asyncio
import contextlib
import json
import logging
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import psutil
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Document, DocumentListResponse, DocumentResponse
from api.services.vector_store import vector_store
from api.utils.text_processing import extract_text_from_file, generate_embedding


# Create a context manager for the ThreadPoolExecutor
@contextlib.contextmanager
def get_executor():
    with ThreadPoolExecutor() as executor:
        yield executor


logger = logging.getLogger(__name__)


def log_memory_usage() -> None:
    process = psutil.Process()
    memory_info = process.memory_info()
    logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")


router = APIRouter()


async def generate_embedding_with_timeout(content, timeout=60) -> Any:
    try:
        logger.info(
            f"Starting generate_embedding_with_timeout, timeout set to {timeout} seconds"
        )
        loop = asyncio.get_event_loop()
        with get_executor() as executor:
            embedding = await asyncio.wait_for(
                loop.run_in_executor(executor, generate_embedding, content),
                timeout=timeout,
            )
        logger.info("generate_embedding_with_timeout completed successfully")
        return embedding
    except asyncio.TimeoutError:
        logger.error("Embedding generation timed out")
        raise HTTPException(
            status_code=500, detail="Embedding generation timed out"
        ) from None
    except Exception as exc:
        logger.error(f"Error in generate_embedding_with_timeout: {str(exc)}")
        raise HTTPException(
            status_code=500, detail="Error generating embedding"
        ) from exc


@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    start_time = time.time()
    log_memory_usage()
    try:
        logger.info(f"Received file: {file.filename}")
        content = await extract_text_from_file(file)
        logger.info(f"Extracted text from file: {file.filename}")
        logger.info(f"Content length: {len(content)} characters")

        logger.info("Starting embedding generation")
        embedding = await generate_embedding_with_timeout(content)
        logger.info(f"Generated embedding for file: {file.filename}")
        logger.info(f"Embedding shape: {embedding.shape}")
        logger.info(f"Embedding generation took {time.time() - start_time:.2f} seconds")

        logger.info("Starting database operation")
        document = Document(
            filename=file.filename,
            content=content,
            embedding=json.dumps(embedding.tolist()),
        )
        logger.info(f"Created document object: {document}")
        db.add(document)
        logger.info("Added document to session")
        db.commit()
        logger.info("Committed session")
        db.refresh(document)
        logger.info(f"Refreshed document, id: {document.id}")
        logger.info(f"Saved document to database: {file.filename}")

        logger.info("Starting vector store operation")
        logger.info(f"Embedding type: {type(embedding)}, shape: {embedding.shape}")
        vector_store.add_document(document.id, embedding)
        logger.info(f"Added document to vector store: {file.filename}")

        return {"message": "Document uploaded successfully"}
    except ValueError as ve:
        logger.error(f"ValueError in upload_document: {str(ve)}")
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while uploading the document",
        )
    finally:
        log_memory_usage()
        logger.info(f"Total upload process took {time.time() - start_time:.2f} seconds")


@router.get("/search", response_model=DocumentListResponse)
async def search_documents(
    query: str, db: Session = Depends(get_db)
) -> DocumentListResponse:
    query_embedding = generate_embedding(query)

    results = vector_store.search(query_embedding, k=5)

    document_ids = [doc_id for doc_id, _ in results]
    documents = db.query(Document).filter(Document.id.in_(document_ids)).all()

    return DocumentListResponse(
        documents=[DocumentResponse.model_validate(doc) for doc in documents]
    )
