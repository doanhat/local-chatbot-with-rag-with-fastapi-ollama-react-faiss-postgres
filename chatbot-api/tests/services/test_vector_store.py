import numpy as np
import pytest

from api.services.vector_store import VectorStore  # Adjust the import to your module


@pytest.fixture
def vector_store():
    # Create a VectorStore instance for testing
    return VectorStore()


def test_add_document(vector_store):
    document_id = "doc1"
    embedding = np.random.random(384)  # Generate a random embedding with 384 dimensions

    # Add the document to the vector store
    vector_store.add_document(document_id, embedding)

    # Assert the document was added
    assert len(vector_store.document_ids) == 1
    assert vector_store.document_ids[0] == document_id


def test_search_empty_store(vector_store):
    query_vector = np.random.random(
        384
    )  # Generate a random query vector with 384 dimensions

    # Search in the empty store, should return an empty list
    result = vector_store.search(query_vector)

    # Assert the result is an empty list
    assert result == []


def test_search_with_documents(vector_store):
    # Add some documents to the vector store
    embeddings = [np.random.random(384) for _ in range(3)]
    document_ids = ["doc1", "doc2", "doc3"]

    for doc_id, emb in zip(document_ids, embeddings):
        vector_store.add_document(doc_id, emb)

    query_vector = embeddings[0]  # Use the embedding of the first document as the query

    # Perform a search
    result = vector_store.search(query_vector, k=2)

    # Assert that the search returns two results
    assert len(result) == 2
    assert result[0][0] == "doc1"  # The closest match should be the first document

    # Assert that the second result is either "doc2" or "doc3" (depending on distance)
    assert result[1][0] in ["doc2", "doc3"]


def test_search_returns_distances(vector_store):
    # Add a document to the vector store
    embedding = np.random.random(384)
    vector_store.add_document("doc1", embedding)

    query_vector = embedding  # Use the same vector as query

    # Perform a search
    result = vector_store.search(query_vector, k=1)

    # Assert that the search returns the correct document with a distance
    assert len(result) == 1
    assert result[0][0] == "doc1"  # Document ID
    assert result[0][1] == pytest.approx(0.0, abs=1e-6)  # Distance should be close to 0


def test_add_document_with_list_embedding(vector_store):
    document_id = "doc1"
    embedding = list(np.random.random(384))  # Use a list instead of a numpy array

    # Add the document to the vector store
    vector_store.add_document(document_id, embedding)

    # Assert the document was added
    assert len(vector_store.document_ids) == 1
    assert vector_store.document_ids[0] == document_id


def test_search_with_list_query(vector_store):
    # Add a document to the vector store
    embedding = np.random.random(384)
    vector_store.add_document("doc1", embedding)

    query_vector = list(embedding)  # Use a list instead of a numpy array for the query

    # Perform a search
    result = vector_store.search(query_vector, k=1)

    # Assert that the search returns the correct document
    assert len(result) == 1
    assert result[0][0] == "doc1"  # Document ID
