from src.utils.LLM import LLM
from src.database.Question import Question
from src.database.Option import Option

import pytest
from hashlib import sha1


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


@pytest.fixture
def sample_messages():
    # Create the initial prompt
    return [
        {
            "role": "system",
            "content": "We are planning a outdoor activity in west Singapore and we need your help. "
            "Can you give us 5 questions one at a time, along with 4 options to vote for. Questions and "
            "votes must be generated based on the previous response except for the first question."
            "After getting votes for the 5 questions, suggest 4 outdoor activity for us to do. "
            "Only give the activity after all voting is done.\n"
            "Format the questions in this manner: \n"
            "Question <x>: <question>\n"
            "1) <option 1>\n"
            "2) <option 2>\n"
            "3) <option 3>\n"
            "4) <option 4>\n"
            "We will tell you the result of our votes in this format: \n"
            "<option 1>) <number of votes for 1>\n"
            "<option 2>) <number of votes for 2>\n"
            "<option 3>) <number of votes for 3>\n"
            "<option 4>) <number of votes for 4>\n"
            "After 5 questions, based on the votes suggest 4 outdoor activity in west "
            "Singapore using this format.\n"
            "Activity x: <activity name>\n"
            "You do not need to show the votes at the end. Only suggest 4 activities after question 5. The "
            "4 activity suggested must be in Singapore and only show me the suggested activities.",
        }
    ]


def test_extract_question_options():
    # create LLM object
    llm = LLM()

    sample_reply = (
        "Question 4: Would your group like to incorporate any food or snacks during the activity? \n"
        "1) Yes, we'd like to have snacks available. \n"
        "2) Yes, we'd like to have a meal included. \n"
    )
    question_text = (
        "Would your group like to incorporate any food or snacks during the activity? "
    )

    extracted_information = llm.extract_question_options(sample_reply)
    assert (
        extracted_information["question_id"]
        == sha1(
            "Would your "
            "group like to incorporate any food or snacks "
            "during the activity? ".encode("utf-8")
        ).hexdigest()
    )
    assert extracted_information["question_text"] == question_text
    assert len(extracted_information["options"]) == 2
    assert (
        extracted_information["options"][0]["option_text"]
        == "Yes, we'd like to have snacks available. "
    )
    assert extracted_information["options"][0]["option_id"] == "1"
    assert (
        extracted_information["options"][1]["option_text"]
        == "Yes, we'd like to have a meal included. "
    )
    assert extracted_information["options"][1]["option_id"] == "2"


def test_generate_llm_reply(sample_question, sample_messages):
    llm = LLM()

    llm_reply = llm.generate_llm_reply(past_questions=[], message=sample_messages)

    llm_reply_past_question = llm.generate_llm_reply(
        past_questions=[sample_question.to_dict()], message=sample_messages
    )
    assert llm_reply[0] == sample_messages[0]
    assert llm_reply_past_question[1] == {
        "role": "assistant",
        "content": "Question 1: What is your favorite color?",
    }
    assert llm_reply_past_question[2] == {
        "role": "user",
        "content": "Red: 0\nBlue: 0\nGreen: 0",
    }


def test_extract_activities(sample_question):
    llm = LLM()

    sample_reply = (
        "Activity 1: Escape Room Challenge at Lost SG\n"
        "Description: activity 1 description\n"
        "Activity 2: Virtual Reality Experience at V-Room\n"
        "Description: activity 2 description\n"
        "Activity 3: Art Jamming Workshop at The Fun Empire\n"
        "Description: activity 3 description\n"
        "Activity 4: Mystery Room Dinner at The Escape Hunt Experience\n"
        "Description: activity 3 description\n"
    )
    activities = llm.extract_activities(sample_reply)

    assert activities["num_of_activity"] == 4
    assert activities["activity: 1"] == "Escape Room Challenge at Lost SG"
    assert activities["activity: 2"] == "Virtual Reality Experience at V-Room"
    assert activities["activity: 3"] == "Art Jamming Workshop at The Fun Empire"
    assert (
        activities["activity: 4"] == "Mystery Room Dinner at The Escape Hunt Experience"
    )


def test_extract_zero_activities(sample_question):
    llm = LLM()

    sample_reply = ""
    activities = llm.extract_activities(sample_reply)

    assert activities["num_of_activity"] == 0
