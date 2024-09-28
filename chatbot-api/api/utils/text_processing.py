import io
import logging
import time
from typing import Any

import docx
import numpy as np
import PyPDF2
import torch
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Force CPU usage
torch.cuda.is_available = lambda: False

# Add this configuration to suppress the warning
model = SentenceTransformer(
    "paraphrase-MiniLM-L3-v2", tokenizer_kwargs={"clean_up_tokenization_spaces": True}
)


async def extract_text_from_file(file) -> str | Any:
    content = await file.read()
    if file.filename.endswith(".pdf"):
        return extract_text_from_pdf(content)
    elif file.filename.endswith(".docx"):
        return extract_text_from_docx(content)
    elif file.filename.endswith(".txt"):
        return content.decode("utf-8")
    else:
        raise ValueError("Unsupported file format")


def extract_text_from_pdf(content: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(content: bytes) -> str:
    doc = docx.Document(io.BytesIO(content))
    return " ".join([paragraph.text for paragraph in doc.paragraphs])


def generate_embedding(text, chunk_size=200) -> np.ndarray:
    try:
        logger.info(f"Starting embedding generation for text of length: {len(text)}")
        start_time = time.time()

        # If text is shorter than chunk_size, use it as is
        if len(text) <= chunk_size:
            chunks = [text]
        else:
            # Split text into chunks
            chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
        logger.info(f"Split text into {len(chunks)} chunks")

        embeddings = []
        for i, chunk in enumerate(chunks):
            chunk_start_time = time.time()
            logger.info(f"Processing chunk {i+1}/{len(chunks)}")

            chunk_embedding = model.encode(chunk)
            embeddings.append(chunk_embedding)

            logger.info(
                f"Processed chunk {i+1} in {time.time() - chunk_start_time:.2f} seconds"
            )

        # Average embeddings from all chunks
        embedding = np.mean(embeddings, axis=0)
        logger.info(f"Generated embedding shape: {embedding.shape}")

        end_time = time.time()
        logger.info(f"Embedding generation took {end_time - start_time:.2f} seconds")

        return embedding
    except Exception as e:
        logger.error(f"Error in generate_embedding: {str(e)}")
        import traceback

        logger.error(traceback.format_exc())
        raise
