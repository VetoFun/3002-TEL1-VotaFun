from src.database.Option import Option


def test_option_creation():
    # Create an Option object
    option = Option(option_id="1", option_text="Option A", current_votes=0)

    # Check if Option attributes are set correctly
    assert option.option_id == "1"
    assert option.option_text == "Option A"
    assert option.current_votes == 0


def test_option_equality():
    # Create two Option objects with the same data
    option1 = Option(option_id="1", option_text="Option A", current_votes=0)
    option2 = Option(option_id="1", option_text="Option A", current_votes=0)

    # Check if the two options are equal
    assert option1 == option2


def test_option_add_vote():
    # Create an Option object
    option = Option(option_id="1", option_text="Option A", current_votes=0)

    # Add votes to the Option
    option.add_vote(num_votes=5)

    # Check if votes are correctly added
    assert option.current_votes == 5


def test_option_set_vote():
    # Create an Option object
    option = Option(option_id="1", option_text="Option A", current_votes=0)

    # Set the vote count for the Option
    option.set_vote(num_votes=10)

    # Check if the vote count is correctly set
    assert option.current_votes == 10


def test_option_to_dict():
    # Create an Option object
    option = Option(option_id="1", option_text="Option A", current_votes=0)

    # Convert the Option to a dictionary
    option_dict = option.to_dict()

    # Check if the resulting dictionary has the expected format
    assert isinstance(option_dict, dict)
    assert option_dict["option_id"] == "1"
    assert option_dict["option_text"] == "Option A"
    assert option_dict["votes"] == 0


def test_option_from_dict():
    # Create a dictionary representing option data
    option_data = {"option_id": "1", "option_text": "Option A", "votes": 5}

    # Create an Option object from the dictionary
    option = Option.from_dict(option_data)

    # Check if the Option object is created correctly
    assert isinstance(option, Option)
    assert option.option_id == "1"
    assert option.option_text == "Option A"
    assert option.current_votes == 5
