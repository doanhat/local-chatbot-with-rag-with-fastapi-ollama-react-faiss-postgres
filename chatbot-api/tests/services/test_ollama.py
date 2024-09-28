from unittest.mock import AsyncMock, patch

import pytest

from api.services.ollama import generate_response, get_available_models
from tests.conftest import TEST_OLLAMA_API_BASE


@pytest.mark.asyncio
async def test_get_available_models_success():
    # Mocking the async HTTP client
    mock_response_data = {"models": ["model1", "model2", "model3"]}

    with patch(
        "httpx.AsyncClient.get",
        new=AsyncMock(
            return_value=AsyncMock(status_code=200, json=lambda: mock_response_data)
        ),
    ), patch("os.getenv", return_value=TEST_OLLAMA_API_BASE):
        # Call the function and verify the result
        result = await get_available_models()
        assert result == mock_response_data["models"]


@pytest.mark.asyncio
async def test_generate_response_success():
    model = "test-model"
    prompt = "test-prompt"

    # Mock valid response stream from the API
    valid_responses = ['{"response": "Hello, "}', '{"response": "world!"}']

    async def mock_aiter_lines():
        for line in valid_responses:
            yield line

    mock_response = AsyncMock()
    mock_response.aiter_lines = mock_aiter_lines
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_response)):
        # Call the function
        result = await generate_response(model, prompt)
        assert result == "Hello, world!"
