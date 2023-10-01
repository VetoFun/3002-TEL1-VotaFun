import openai
import re
from hashlib import sha1

from src.database.Option import Option
from src.database.Question import Question
from src.logger import logger


class LLM:
    def __init__(self):
        # regexes to extract information Chatgpt returns
        self.activity_regex = r"Activity \d+: (.+)"
        self.question_regex = r"Question \d+: (.+)"
        # self.option_regex = r"[0-9]\).*"
        self.option_regex = r"[0-9]\) (.+)"

    def get_reply(self, room_id, database):
        # get room properties
        room = database.query_room_data(room_id, True)
        room_location = room["room_location"]
        room_activity = room["room_activity"]

        # initial prompt
        messages = [
            {
                "role": "system",
                "content": f"We are planning a {room_activity} activity in {room_location} Singapore and we need your "
                f"help. Can you give us 5 questions one at a time, along with 4 options to vote for. Questions and "
                f"votes must be generated based on the previous response except for the first question."
                f"After getting votes for the 5 "
                f"questions, suggest 4 {room_activity} activity for us to do. Only give the activity after "
                f"all voting is done.\n"
                f"Format the questions in this manner: \n"
                f"Question <x>: <question>\n"
                f"1) <option 1>\n"
                f"2) <option 2>\n"
                f"3) <option 3>\n"
                f"4) <option 4>\n"
                f"We will tell you the result of our votes in this format: \n"
                f"<option 1>) <number of votes for 1>\n"
                f"<option 2>) <number of votes for 2>\n"
                f"<option 3>) <number of votes for 3>\n"
                f"<option 4>) <number of votes for 4>\n"
                f"After 5 questions, based on the votes suggest 4 {room_activity} activity in {room_location} "
                f"Singapore using this format.\n"
                f"Activity x: <activity name>\n"
                f"You do not need to show the votes at the end. Only suggest 4 activities after question 5. The "
                f"4 activity suggested must be in Singapore and only show me the suggested activities.",
            }
        ]

        # adding the past questions asked by chatGPT and their votes
        past_questions = room["questions"]
        # got the reply we need, send it to the llm
        message_to_send = self.generate_llm_reply(
            past_questions=past_questions, message=messages
        )
        # the reply from chatgpt
        llm_reply = self.call_gpt(messages=message_to_send)

        # extracted information
        question_and_options = self.extract_question_options(llm_reply=llm_reply)
        activities = self.extract_activities(llm_reply=llm_reply)

        # llm returned activity options we return it
        if activities["num_of_activity"] != 0:
            return activities, "activity"
        else:
            # todo: tell chatgpt to regenerate if there is no options
            # todo: store questions and options
            # todo: update room activity time
            return question_and_options, "question"

    def generate_llm_reply(self, past_questions, message):
        # given the past questions the llm asked, generate a new message to ask the llm
        # sockets will be handling each time a user votes, so we can iterate through all questions,
        # extracting the questions, and number of votes.

        # the room will have 0 past question if it is their first question.
        if len(past_questions) != 0:
            for i in range(0, len(past_questions)):
                questions = {
                    "role": "assistant",
                    "content": f"Question {i + 1}: "
                    + past_questions[i]["question_text"],
                }

                question_options = past_questions[i]["options"]

                content = ""
                for option in question_options:
                    content += f"{option['option_text']}: {option['votes']}\n"

                votes_question = {
                    "role": "user",
                    "content": content[:-1],
                }
                message.append(questions)
                message.append(votes_question)
        logger.info(message)
        return message

    def call_gpt(self, messages):
        # calling chatGPT API
        try:
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
            chatgpt_reply = chat.choices[0].message["content"]
        except Exception:
            raise

        logger.info(f"{chatgpt_reply}")
        return chatgpt_reply

    def extract_question_options(self, llm_reply):
        question_matches = re.findall(self.question_regex, llm_reply)
        option_matches = re.findall(self.option_regex, llm_reply)

        try:
            options_list = []
            for i in range(len(option_matches)):
                option = Option(option_id=str(i + 1), option_text=option_matches[i])
                options_list.append(option)

            question_id = sha1(question_matches[0].encode("utf-8")).hexdigest()
            question = Question(
                question_id=question_id,
                question_text=question_matches[0],
                options=options_list,
            )

            print(question.to_dict())
            return question.to_dict()
        except Exception:
            raise ValueError("Could not extract questions or options")

    def extract_activities(self, llm_reply):
        # format into a json that can be emitted
        activities_matches = re.findall(self.activity_regex, llm_reply)

        activities = {}

        for i in range(len(activities_matches)):
            activities[f"activity: {i + 1}"] = activities_matches[i]
        activities["num_of_activity"] = len(activities_matches)
        return activities

    def retry_logic(self):
        pass
