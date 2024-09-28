from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from api.models import ChatHistory, Document
from api.services.vector_store import vector_store


@pytest.fixture
def mock_generate_response():
    with patch("api.routers.chat.generate_response", new_callable=AsyncMock) as mock:
        mock.return_value = "Mocked response"
        yield mock


@pytest.fixture
def mock_generate_embedding():
    with patch("api.routers.chat.generate_embedding") as mock:
        mock.return_value = [0.1, 0.2, 0.3]
        yield mock


@pytest.fixture
def mock_vector_store():
    with patch("api.routers.chat.vector_store") as mock:
        mock.search.return_value = [(1, 0.9)]
        yield mock


def test_chat_endpoint(
    client: TestClient,
    test_db_session,
    setup_database,
    mock_generate_response,
    mock_generate_embedding,
    mock_vector_store,
):
    response = client.post(
        "/api/chat", json={"message": "Hello", "model": "test-model"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Mocked response"}

    mock_generate_embedding.assert_called_once_with("Hello")
    mock_vector_store.search.assert_called_once()
    mock_generate_response.assert_called_once()

    # Check if chat history was added to the database
    chat_history = (
        test_db_session.query(ChatHistory).filter_by(user_input="Hello").first()
    )
    assert chat_history is not None
    assert chat_history.bot_response == "Mocked response"


def test_get_chat_history(client: TestClient, test_db_session, setup_database):
    response = client.get("/api/chat/history")

    assert response.status_code == 200
    chat_history = response.json()["chat_history"]
    assert len(chat_history) > 0
    assert chat_history[0]["user_input"] == "Test input"
    assert chat_history[0]["bot_response"] == "Test response"


def test_chat_endpoint_with_document(
    client: TestClient,
    test_db_session,
    setup_database,
    mock_generate_response,
    mock_generate_embedding,
    mock_vector_store,
):
    response = client.post(
        "/api/chat",
        json={"message": "What's in the test document?", "model": "test-model"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Mocked response"}

    mock_generate_embedding.assert_called_once_with("What's in the test document?")
    mock_vector_store.search.assert_called_once()
    mock_generate_response.assert_called_once()

    # Check if the document was retrieved
    call_args = mock_generate_response.call_args[0][1]
    assert "This is a test document" in call_args
