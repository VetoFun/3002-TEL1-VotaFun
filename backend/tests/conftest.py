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


# Create the Flask app for testing
@pytest.fixture(scope="function")
def test_client(mock_redis):
    app = create_app()
    with app.test_client() as client:
        client.database = mock_redis
        yield client
