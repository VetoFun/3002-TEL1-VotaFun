import pytest
from src.database import Question, Option


@pytest.fixture
def sample_question():
    # Create a sample question for testing
    return Question(
        question_id="q1",
        question_text="What is your favorite color?",
        options=[
            Option(option_id="o1", option_text="Red"),
            Option(option_id="o2", option_text="Blue"),
            Option(option_id="o3", option_text="Green"),
        ],
    )


def test_question_creation():
    # Create an Option object
    question = Question(
        question_id="q1",
        question_text="What is your favorite color?",
        options=[
            Option(option_id="o1", option_text="Red"),
            Option(option_id="o2", option_text="Blue"),
            Option(option_id="o3", option_text="Green"),
        ],
    )

    # Check if Option attributes are set correctly
    assert question.question_id == "q1"
    assert question.question_text == "What is your favorite color?"
    assert question.options == [
        Option(option_id="o1", option_text="Red"),
        Option(option_id="o2", option_text="Blue"),
        Option(option_id="o3", option_text="Green"),
    ]


def test_question_equality(sample_question):
    # Create two Option objects with the same data
    question1 = Question(
        question_id="q1",
        question_text="What is your favorite color?",
        options=[
            Option(option_id="o1", option_text="Red"),
            Option(option_id="o2", option_text="Blue"),
            Option(option_id="o3", option_text="Green"),
        ],
    )

    # Check if the two options are equal
    assert question1 == sample_question


def test_add_option(sample_question):
    # Test adding an option to the question
    new_option = Option(option_id="o4", option_text="Yellow")
    sample_question.add_option(new_option)
    assert len(sample_question.options) == 4


def test_get_option_by_id(sample_question):
    # Test getting an option from the question by option ID
    retrieved_option = sample_question.get_option_by_id("o2")
    assert retrieved_option.option_id == "o2"
    assert retrieved_option.option_text == "Blue"


def test_get_option_by_id_not_found(sample_question):
    # Test getting an option that doesn't exist
    with pytest.raises(KeyError):
        sample_question.get_option_by_id("non_existent_option")


def test_to_dict(sample_question):
    # Test converting the question to a dictionary
    question_dict = sample_question.to_dict()
    assert isinstance(question_dict, dict)
    assert question_dict["question_id"] == "q1"
    assert question_dict["question_text"] == "What is your favorite color?"
    assert len(question_dict["options"]) == 3  # 3 options in the sample


def test_from_dict():
    # Test creating a question from a dictionary
    question_dict = {
        "question_id": "q2",
        "question_text": "What is your favorite animal?",
        "options": [
            {"option_id": "o5", "option_text": "Dog"},
            {"option_id": "o6", "option_text": "Cat"},
        ],
    }
    question = Question.from_dict(question_dict)
    assert isinstance(question, Question)
    assert question.question_id == "q2"
    assert question.question_text == "What is your favorite animal?"
    assert len(question.options) == 2  # 2 options in the dictionary
