import json
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from fastapi.testclient import TestClient

from api.models import Document


@pytest.fixture
def mock_extract_text():
    with patch("api.routers.documents.extract_text_from_file") as mock:
        mock.return_value = "Mocked document content"
        yield mock


@pytest.fixture
def mock_generate_embedding():
    with patch("api.routers.documents.generate_embedding_with_timeout") as mock:
        mock.return_value = np.array([0.1, 0.2, 0.3])
        yield mock


@pytest.fixture
def mock_vector_store():
    with patch("api.routers.documents.vector_store") as mock:
        mock.search.return_value = [(1, 0.9)]
        yield mock


def test_upload_document(
    client: TestClient,
    test_db_session,
    mock_extract_text,
    mock_generate_embedding,
    mock_vector_store,
):
    file_content = b"Test file content"
    files = {"file": ("test.pdf", file_content, "application/pdf")}

    response = client.post("/api/documents/upload", files=files)

    assert response.status_code == 200
    assert response.json() == {"message": "Document uploaded successfully"}

    mock_extract_text.assert_called_once()
    mock_generate_embedding.assert_called_once()
    mock_vector_store.add_document.assert_called_once()

    # Check if document was added to the database
    document = test_db_session.query(Document).filter_by(filename="test.pdf").first()
    assert document is not None
    assert document.content == "Mocked document content"
    assert json.loads(document.embedding) == [0.1, 0.2, 0.3]


def test_search_documents(
    client: TestClient,
    mock_vector_store,
):
    response = client.get("/api/documents/search?query=test")

    assert response.status_code == 200
    documents = response.json()["documents"]
    assert len(documents) > 0
    assert documents[0]["filename"] == "test.txt"
    assert documents[0]["content"] == "This is a test document."

    mock_vector_store.search.assert_called_once()


def test_upload_document_extraction_error(client: TestClient, mock_extract_text):
    mock_extract_text.side_effect = ValueError("Unsupported file format")

    file_content = b"Test file content"
    files = {"file": ("test.unsupported", file_content, "application/octet-stream")}

    response = client.post("/api/documents/upload", files=files)

    assert response.status_code == 500
    assert "Unsupported file format" in response.json()["detail"]
