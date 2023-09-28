import pytest
from src.database import Room, RoomStatus, User, Question, Option

TEST_USERS = [User(user_id="a1", user_name="Alp")]
TEST_QUESTIONS = [
    Question(
        question_id="q1",
        question_text="What is your favorite color?",
        options=[
            Option(option_id="o1", option_text="Red"),
            Option(option_id="o2", option_text="Blue"),
            Option(option_id="o3", option_text="Green"),
        ],
    )
]
TEST_NUM_OF_USER = len(TEST_USERS)
TEST_MAX_CAPACITY = 10


@pytest.fixture
def sample_room_data():
    # Create a sample Room object for testing
    return Room(
        room_id="room1",
        number_of_user=TEST_NUM_OF_USER,
        max_capacity=TEST_MAX_CAPACITY,
        last_activity="2023-09-22 12:00:00",
        questions=TEST_QUESTIONS,
        host_id="host1",
        status=RoomStatus.WAITING,
        room_location="Location1",
        room_activity="Activity1",
        users=TEST_USERS,
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


def test_add_user(mock_redis, sample_room_data):
    # Test adding user to database
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    # Test adding a user
    users = mock_redis.add_user(room_id=room_id, user_id="u3", username="Charles")

    # Query the room data
    queried_room = mock_redis.query_room_data(sample_room_data.room_id)

    assert queried_room.users == users


def test_add_user_max(mock_redis, sample_room_data):
    # Test adding user when it's already maxed
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )
    for i in range(TEST_MAX_CAPACITY - 1):
        mock_redis.add_user(room_id=room_id, user_id="u3", username="Charles")

    # Check that the room still has only max users
    assert len(mock_redis.get_users(room_id=room_id)) == TEST_MAX_CAPACITY
    # Add one more, which should raise an exception
    with pytest.raises(Exception):
        mock_redis.add_user(room_id=room_id, user_id="u3", username="Charles")


def test_get_users(mock_redis, sample_room_data):
    # Test getting users
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    users = mock_redis.get_users(sample_room_data.room_id)

    # Check that the user is in the list of users
    assert len(TEST_USERS) == len(mock_redis.get_users(room_id=room_id))
    assert users[0]["user_id"] == TEST_USERS[0].user_id


def test_remove_users(mock_redis, sample_room_data):
    # Test removing users
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    result, _ = mock_redis.remove_user(sample_room_data.room_id, TEST_USERS[0].user_id)

    # Check that the operation was successful
    assert result == 0


def test_get_questions(mock_redis, sample_room_data):
    # Test getting questions
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )
    questions = mock_redis.get_questions(sample_room_data.room_id)
    assert len(questions) == len(TEST_QUESTIONS)
    assert questions[0]["question_id"] == TEST_QUESTIONS[0].question_id


def test_add_question_and_options(mock_redis, sample_room_data):
    # Test adding questions and options
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )
    question2 = Question(
        question_id="q3",
        question_text="What's your favorite animal?",
        options=[("o1", "dinosaur")],
    )

    # Test inserting a question
    mock_redis.add_question_and_options(
        room_id=room_id,
        question_id=question2.question_id,
        question_text=question2.question_text,
        options=question2.options,
    )

    # Check that the operation was successful
    questions = mock_redis.get_questions(sample_room_data.room_id)
    assert len(questions) == len(TEST_QUESTIONS) + 1


def test_get_options(mock_redis, sample_room_data):
    # Test getting options
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    options = mock_redis.get_options(room_id, sample_room_data.questions[0].question_id)

    # Check that the option is in the list of options
    assert len(options) == len(TEST_QUESTIONS[0].options)
    assert options[0]["option_id"] == TEST_QUESTIONS[0].options[0].option_id


def test_add_option(mock_redis, sample_room_data):
    # Test adding options
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    # Call the add_option function
    result = mock_redis.add_option(
        room_id=room_id,
        question_id=sample_room_data.questions[0].question_id,
        option_id="new_option",
        option_text="New Option",
    )

    # Check if the result is as expected
    assert result == len(sample_room_data.questions[0].options) + 1


def test_get_vote(mock_redis, sample_room_data):
    # Test getting vote
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    # Call the get_vote function
    result = mock_redis.get_vote(
        room_id=room_id,
        question_id=sample_room_data.questions[0].question_id,
        option_id=sample_room_data.questions[0].options[0].option_id,
    )

    # Check if the result is as expected
    assert result == sample_room_data.questions[0].options[0].current_votes


def test_increment_vote(mock_redis, sample_room_data):
    # Test function for increment_vote
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    # Call the increment_vote function
    result = mock_redis.increment_vote(
        room_id=sample_room_data.room_id,
        question_id=sample_room_data.questions[0].question_id,
        option_id=sample_room_data.questions[0].options[0].option_id,
        num_votes=2,
    )

    # Check if the result is as expected
    assert result == sample_room_data.questions[0].options[0].current_votes + 2


def test_set_vote(mock_redis, sample_room_data):
    # Test function for set_vote
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    # Call the set_vote function
    result = mock_redis.set_vote(
        room_id=room_id,
        question_id=sample_room_data.questions[0].question_id,
        option_id=sample_room_data.questions[0].options[0].option_id,
        num_votes=5,
    )

    # Check if the result is as expected
    assert result == 5  # Assuming you set the vote count to 5


def test_update_room_activity_time(mock_redis, sample_room_data):
    # Test update room activity time
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    # Call the update_room_activity_time function
    new_activity_time = "2023-09-28 15:49:00"
    result = mock_redis.update_room_activity_time(
        room_id=room_id, activity_time=new_activity_time
    )

    # Check if the result is as expected
    assert result == new_activity_time


def test_query_room_id_from_user_id(mock_redis, sample_room_data):
    # Test function for query_room_id_from_user_id
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    # Call the query_room_id_from_user_id function
    user_id = TEST_USERS[0].user_id
    result = mock_redis.query_room_id_from_user_id(user_id)

    # Check if the result is as expected
    assert result == sample_room_data.room_id


def test_create_room(mock_redis):
    # Test function for create_room
    # Call the create_room function
    result = mock_redis.create_room()

    # Check if the result is a valid room_id (string)
    assert isinstance(result, str)


def test_change_host(mock_redis, sample_room_data):
    # Test function for change_host
    pipeline = mock_redis.r.pipeline()
    room_id = sample_room_data.room_id

    # Store sample room data in Redis
    mock_redis.store_room_data(
        room_id=room_id, room_data=sample_room_data, pipeline=pipeline
    )

    # Call the change_host function
    new_host_id = "new_host"
    mock_redis.change_host(
        room_id=room_id,
        new_host_id=new_host_id,
    )

    # Retrieve the updated room data
    updated_room_data = mock_redis.query_room_data(sample_room_data.room_id)

    # Check if the host_id has been updated
    assert updated_room_data.host_id == new_host_id
