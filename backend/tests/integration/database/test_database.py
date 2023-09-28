import pytest
from src.database import Room, RoomStatus


@pytest.fixture
def sample_room_data():
    # Create a sample Room object for testing
    return Room(
        room_id="room1",
        number_of_user=3,
        max_capacity=10,
        last_activity="2023-09-22 12:00:00",
        questions=[],
        host_id="host1",
        status=RoomStatus.WAITING,
        room_location="Location1",
        room_activity="Activity1",
        users=[],
    )


def test_query_room_data_with_existing_room(mock_redis, sample_room_data):
    # Test querying room data for an existing room
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    # Query the room data
    retrieved_room = mock_redis.query_room_data(room_id=room_id, return_dict=False)

    # Assert that the retrieved room matches the sample data
    assert retrieved_room == sample_room_data


def test_query_existing_room_data_return_dict(mock_redis, sample_room_data):
    room_id = sample_room_data.room_id
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=mock_redis.r.pipeline()
    )
    room_data_dict = mock_redis.query_room_data(room_id=room_id, return_dict=True)

    # Verify that room_data_dict is a dictionary and matches the sample data
    assert isinstance(room_data_dict, dict)
    sample_data = sample_room_data.to_dict()
    assert room_data_dict == sample_data


def test_query_room_data_with_nonexistent_room(mock_redis):
    # Test querying room data for a non-existing room
    room_id = "non_existent_room"

    # Attempt to query the room data for a room that doesn't exist
    with pytest.raises(KeyError):
        mock_redis.query_room_data(room_id=room_id)


def test_store_room_data(mock_redis, sample_room_data):
    # Test storing room data in Redis
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    # Check if the data was stored correctly in Redis
    room_data_in_redis = mock_redis.r.hgetall(room_id)
    assert len(room_data_in_redis) > 0  # Data exists in Redis

    # Clean up: delete the room data from Redis
    mock_redis.r.delete(room_id)
    assert not mock_redis.r.exists(room_id)  # Room data is deleted