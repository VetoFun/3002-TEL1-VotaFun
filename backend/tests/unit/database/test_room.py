import pytest
from datetime import datetime, timedelta
from src.database import Room, User, RoomStatus, Question


@pytest.fixture
def sample_room():
    # Create a sample room for testing
    return Room(
        room_id="test_room",
        number_of_user=0,
        max_capacity=10,
        last_activity=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        questions=[],
        host_id="",
        status=RoomStatus.WAITING,
        room_location="",
        room_activity="",
        users=[],
    )


def test_add_user(sample_room):
    # Test adding a user to the room
    user = User(user_id="user_id", user_name="John")
    sample_room.add_user(user)
    assert len(sample_room.users) == 1
    assert sample_room.number_of_user == 1


def test_remove_user_from_id(sample_room):
    # Test removing a user from the room by user ID
    user = User(user_id="user_id", user_name="John")
    sample_room.add_user(user)
    sample_room.remove_user_from_id(user_id="user_id")
    assert len(sample_room.users) == 0
    assert sample_room.number_of_user == 0


def test_get_question_from_id(sample_room):
    # Test getting a question from the room by question ID
    question = Question(question_id="q1", question_text="What is your name?")
    sample_room.add_question(question)
    retrieved_question = sample_room.get_question_from_id("q1")
    assert retrieved_question == question


def test_get_question_from_id_not_found(sample_room):
    # Test getting a question that doesn't exist
    with pytest.raises(KeyError):
        sample_room.get_question_from_id("non_existent_question")


def test_get_user_from_id(sample_room):
    # Test getting a user from the room by user ID
    user = User(user_id="user_id", user_name="John")
    sample_room.add_user(user)
    retrieved_user = sample_room.get_user_from_id("user_id")
    assert retrieved_user == user


def test_get_user_from_id_not_found(sample_room):
    # Test getting a user that doesn't exist
    with pytest.raises(KeyError):
        sample_room.get_user_from_id("non_existent_user")


def test_start_room(sample_room):
    # Test starting the room
    sample_room.start_room()
    assert sample_room.status == RoomStatus.STARTED


def test_is_room_still_active(sample_room):
    # Test checking if the room is still active
    now = datetime.now()
    assert sample_room.is_room_still_active(now)

    # Simulate inactivity for more than 1 hour
    inactive_time = now - timedelta(hours=2)
    sample_room.last_activity = inactive_time.strftime("%Y-%m-%d %H:%M:%S")
    assert not sample_room.is_room_still_active(now)


def test_to_dict(sample_room):
    # Test converting the room to a dictionary
    room_dict = sample_room.to_dict()
    assert isinstance(room_dict, dict)
    assert room_dict["room_id"] == "test_room"
    assert room_dict["number_of_user"] == 0
    # Add more assertions for other attributes


def test_from_dict():
    # Test creating a room from a dictionary
    room_dict = {
        "room_id": "test_room",
        "number_of_user": 5,
        # Add more attributes
    }
    room = Room.from_dict(room_dict)
    assert isinstance(room, Room)
    assert room.room_id == "test_room"
    assert room.number_of_user == 5
