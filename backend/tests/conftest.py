import os
import pytest
from datetime import datetime

from src.app import create_app
from src.database import Database
from src.database.Room import Room, RoomStatus


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


# A sample room for testing
@pytest.fixture(scope="function")
def sample_room():
    # Create a sample room for testing
    last_activity = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    yield Room(
        room_id="test_room",
        number_of_user=0,
        max_capacity=10,
        last_activity=last_activity,
        questions=[],
        host_id="",
        status=RoomStatus.WAITING,
        room_location="",
        room_activity="",
        users=[],
    )
