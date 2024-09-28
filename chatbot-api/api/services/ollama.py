import json
import logging
import os

import httpx
from fastapi import HTTPException  # Import HTTPException

from api.config.env import OLLAMA_API_BASE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_available_models() -> list:
    url = f"{OLLAMA_API_BASE}/api/tags"

    logger.info(f"Attempting to connect to Ollama at: {url}")
    logger.info(f"Current OLLAMA_API_BASE: {OLLAMA_API_BASE}")
    logger.info(f"Environment OLLAMA_API_BASE: {os.getenv('OLLAMA_API_BASE')}")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            logger.info(f"Fetching models from {url}")
            response = await client.get(url)
            response.raise_for_status()

            data = response.json()
            models = data.get("models", [])
            logger.info(f"Fetched models: {models}")
            return models
    except httpx.ConnectError as ex:
        logger.error(f"Failed to connect to Ollama at {url}. Is it running?")
        raise HTTPException(
            status_code=503,
            detail=f"Ollama service is not available at {url}. Please check if it's running and accessible.",
        ) from ex
    except httpx.HTTPStatusError as ex:
        logger.error(f"HTTP error occurred: {ex}")
        raise HTTPException(
            status_code=ex.response.status_code,
            detail=f"Error from Ollama service: {ex.response.text}",
        ) from ex
    except Exception as ex:
        logger.error(f"Unexpected error occurred: {ex}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while connecting to Ollama: {str(ex)}",
        ) from ex


async def generate_response(model: str, prompt: str, timeout: float = 60.0) -> str:
    url = f"{OLLAMA_API_BASE}/api/generate"  # Updated to use OLLAMA_API_BASE
    payload = {"model": model, "prompt": prompt}

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()

            full_response = ""
            async for line in response.aiter_lines():
                try:
                    data = json.loads(line)
                    if "response" in data:
                        full_response += data["response"]
                except json.JSONDecodeError:
                    continue

            if not full_response:
                raise ValueError("No valid response received from Ollama API")

            return full_response

    except httpx.ReadTimeout:
        return "I'm sorry, but the response is taking longer than expected. Please try again or try a shorter prompt."
    except httpx.HTTPStatusError as e:
        return f"An error occurred while communicating with the Ollama API: {str(e)}"
    except httpx.ConnectError:
        logger.error("Failed to connect to Ollama. Is it running?")
        return "I'm sorry, but I'm unable to connect to the language model service at the moment. Please try again later."
