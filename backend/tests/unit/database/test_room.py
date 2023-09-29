import pytest
from datetime import datetime, timedelta
from src.database import Room, User, RoomStatus, Question


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


def test_add_question(sample_room):
    # Test adding a question to the room
    question = Question(question_id="q1", question_text="What is your name?")
    sample_room.add_question(question)

    # Check if the question was added to the room
    assert len(sample_room.questions) == 1
    assert sample_room.questions[0] == question


def test_get_number_of_user(sample_room):
    # Test getting the number of users in the room
    assert sample_room.get_number_of_user() == 0

    # Add a user to the room
    user = User(user_id="user_id", user_name="John")
    sample_room.add_user(user)

    # Check if the number of users is updated
    assert sample_room.get_number_of_user() == 1


def test_get_max_capacity(sample_room):
    # Test getting the maximum capacity of the room
    assert sample_room.get_max_capacity() == 10


def test_set_host(sample_room):
    # Test setting the host of the room
    assert sample_room.host_id == ""

    # Set a new host
    new_host_id = "new_host"
    sample_room.set_host(new_host_id)

    # Check if the host is updated
    assert sample_room.host_id == new_host_id


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
