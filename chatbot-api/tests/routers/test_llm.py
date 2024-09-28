from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def mock_get_available_models():
    with patch("api.routers.llm.get_available_models", new_callable=AsyncMock) as mock:
        mock.return_value = ["model1", "model2", "model3"]
        yield mock


def test_list_models(client: TestClient, mock_get_available_models):
    response = client.get("/api/models")

    assert response.status_code == 200
    assert response.json() == {"models": ["model1", "model2", "model3"]}

    mock_get_available_models.assert_called_once()
