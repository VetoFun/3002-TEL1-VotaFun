from src.database.User import User


def test_user_creation():
    # Create a User object
    user = User(user_id="123", user_name="Alice")

    # Check if user attributes are set correctly
    assert user.user_id == "123"
    assert user.user_name == "Alice"


def test_user_equality():
    # Create two User objects with the same data
    user1 = User(user_id="123", user_name="Alice")
    user2 = User(user_id="123", user_name="Alice")

    # Check if the two users are equal
    assert user1 == user2


def test_user_to_dict():
    # Create a User object
    user = User(user_id="123", user_name="Alice")

    # Convert the user to a dictionary
    user_dict = user.to_dict()

    # Check if the resulting dictionary has the expected format
    assert isinstance(user_dict, dict)
    assert user_dict["user_id"] == "123"
    assert user_dict["user_name"] == "Alice"


def test_user_from_dict():
    # Create a dictionary representing user data
    user_data = {"user_id": "123", "user_name": "Alice"}

    # Create a User object from the dictionary
    user = User.from_dict(user_data)

    # Check if the User object is created correctly
    assert isinstance(user, User)
    assert user.user_id == "123"
    assert user.user_name == "Alice"
