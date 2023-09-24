import os
import pytest

from src.app import create_app
from src.database import Database


# Mock Redis connection for testing
@pytest.fixture(scope="function")
def mock_redis():
    redis_url = os.environ.get("REDIS_URL", "redis://@localhost:6379")
    redis_client = Database(redis_url=redis_url)
    redis_client.r.flushdb()  # Flush the database
    yield redis_client
    redis_client.r.flushdb()  # Flush the database again after each test


# Create the Flask app for testing
@pytest.fixture(scope="function")
def test_app():
    app = create_app(testing=True)  # Pass testing=True to use the TestingConfig
    yield app


# Create a test client for the Flask app
@pytest.fixture(scope="function")
def test_client(test_app, mock_redis):
    with test_app.test_client() as client:
        client.database = mock_redis
        yield client
