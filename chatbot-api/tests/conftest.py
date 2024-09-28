import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.database import Base, get_db
from api.main import create_app
from api.models import ChatHistory, Document

# Use in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
TEST_OLLAMA_API_BASE = "test_ollama_api_base"


@pytest.fixture(scope="function")
def test_engine():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_db_session(test_engine):
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(test_engine, test_db_session):
    def override_get_db():
        try:
            yield test_db_session
        finally:
            test_db_session.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def setup_database(test_db_session):
    # Create test data
    document = Document(filename="test.txt", content="This is a test document.")
    test_db_session.add(document)
    test_db_session.commit()

    chat_history = ChatHistory(
        user_input="Test input", bot_response="Test response", model="test-model"
    )
    test_db_session.add(chat_history)
    test_db_session.commit()

    yield

    # Clean up after the test
    test_db_session.query(ChatHistory).delete()
    test_db_session.query(Document).delete()
    test_db_session.commit()
