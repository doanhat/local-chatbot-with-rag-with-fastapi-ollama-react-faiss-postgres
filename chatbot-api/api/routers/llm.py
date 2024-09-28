import logging

from fastapi import APIRouter

from api.services.ollama import get_available_models

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def list_models() -> dict[str, list]:
    logger.info("Fetching models")
    models = await get_available_models()
    logger.info(f"Returning models: {models}")
    return {"models": models}
