import os

import openai
import re
from hashlib import sha1

from src.database.Option import Option
from src.database.Question import Question
from src.logger import logger


class LLM:
    def __init__(self):
        # regexes to extract information Chatgpt returns
        self.activity_regex = r"[Activity|Location] \d+: (.+)"
        self.question_regex = r"Question \d+: (.+)"
        self.option_regex = r"[0-9]\) (.+)\b"
        # sets the api key
        openai.api_key = os.getenv("OPENAI_API_KEY", "")

        # re prompts
        self.re_prompt = (
            "\nWe are indecisive so give us a properly formatted question "
            "with 4 options to vote. Remember ask unique questions and options. "
            "Format the questions in this manner: \n"
            "Question <x>: <question>\n"
            "1) <option 1>\n"
            "2) <option 2>\n"
            "3) <option 3>\n"
            "4) <option 4>\n"
        )

    def get_reply(self, room_id, database):
        # get room properties
        room = database._query_room_data(room_id)
        # set last_activity of the room
        room.set_last_activity()
        room_location = room.get_room_location()
        room_activity = room.get_room_activity()

        # initial prompt
        messages = [
            {
                "role": "system",
                "content": f"We are a group of friends planning for {room_activity} activity in {room_location} "
                f"Singapore and we need your help to figure out the details of our activity."
                f"Can you give us a series of 5 questions, namely what, where, when to help us pinpoint the at "
                f"a specific location?"
                f"Each question should help narrow down our choices to a single location in {room_location} Singapore,"
                f"where we can carry out our {room_activity} activity"
                f"Please avoid asking how far should an activity be, or when it should take place."
                f"Each question should provide 4-6 diverse options for us to vote for."
                f"""{'For Food Activity, we would like to have a meal somewhere in Singapore and need your help to decide where to eat.'
                    if room_activity == 'Food' else ''}"""
                f"""{'Do consider that some of our friends may have dietary restrictions and one of the questions '
                     'should ask for them (ie. Halal, Vegan).' if room_activity == 'Food' else ''}"""
                f"""{'Do suggest a cuisine found here in Singpoare (especially food from East Asia) '
                     'in Singapore. ' if room_activity == 'Food' else ''}"""
                f"""{'Do ask what type of activity we would like to play.' if room_activity == 'Fun' else ''}"""
                f"""{'Avoid giving an option for virtual activity, the location must be physical'
                     '.' if room_activity == 'Fun' else ''}"""
                f"""{'Do give a specific address if we are voting for a location.'
                     '.' if room_activity == 'Fun' else ''}"""
                f"""{'Do ask what type of leisure activity we would like to '
                     'do.' if room_activity == 'Leisure' else ''}"""
                f"Please avoid providing repetitive or similar questions."
                f"Format the questions in this manner: \n"
                f"Question <x>: <question>\n"
                f"<number y>) <option y>\n"
                f"We will tell you the result of our votes in this format: \n"
                f"<option y>) <number of votes for y>\n"
                f"Most importantly, do not repeat any questions and options. Be concise when generating options, "
                f"preferably within 10 words. Do ask one question at a time.",
            }
        ]

        # final prompt once 5 questions is asked.
        final_prompt = (
            f"\nWe have provided our preferences for the kind of activity we would like to pursue."
            f"Based on the voting results, can you recommend us 4 "
            f"locations in {room_location} Singapore that we can enjoy our {room_activity} activities in? "
            f"""{f'Do give specific {room_activity} activity we should do based on the voting '
                 f'results.' if room_activity == 'Fun' or room_activity == 'Leisure' else ''}"""
            f"Format the activities in this manner.\n"
            f"Activity 1: Activity name (address)\n"
            f"Activity 2: Activity name (address)\n"
            f"Activity 3: Activity name (address)\n"
            f"Activity 4: Activity name (address)\n"
            f"Please provide the location name and address within the same line.\n"
            f"Please be specific in the details of the location, namely the name of the location and the address.\n"
            f"Remember the location must be in {room_location} Singapore, and the {room_activity} activity "
            f"recommended must be based off our choices. Do not ask us anymore questions."
        )

        # getting the past questions asked by chatGPT and their votes
        past_questions = room.get_questions()
        # formatted the reply we need, send it to the llm
        message_to_send = self.generate_llm_reply(
            past_questions=past_questions, message=messages, final_prompt=final_prompt
        )
        # the reply from chatgpt
        llm_reply = self.call_gpt(messages=message_to_send)

        # extract information
        question_and_options = self.extract_question_options(llm_reply=llm_reply)
        # llm returned questions and options we extract it
        if question_and_options is not None:
            # tell chatgpt to regenerate if there is < 2 options
            if len(question_and_options.to_dict()["options"]) < 2:
                question_and_options = self.retry_logic(message=message_to_send)
            # store the questions and room data
            database.add_question_and_options(room, question_and_options)
            return question_and_options.to_dict(), "question"
        # llm returned activity options we extract it
        else:
            activities = self.extract_activities(llm_reply=llm_reply)
            question_text = "Which activity would you like to do?"
            question_id = sha1(question_text.encode("utf-8")).hexdigest()
            question = Question(
                question_id=question_id,
                question_text=question_text,
                options=activities["activities"],
                last_question=True,
            )
            database.add_question_and_options(room, question)
            return question.to_dict(), "activity"

    def generate_llm_reply(self, past_questions, message, final_prompt):
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

            if len(past_questions) == 5:
                # once 5 questions is asked, force ChatGPT to give us some activities.
                message[-1]["content"] += final_prompt
            else:
                # adding the re prompt to ensure that llm almost always gives us what is expected.
                message[-1]["content"] += self.re_prompt
        logger.info(message)
        return message

    # def summarize_votes(self, question, votes):
    #     content = f"Given the following question: '{question}'\nCould you provide a summary in one sentence of the
    #     following options that we have voted on?\n"
    #     for option in votes:
    #         content += f"{option['option_text']}: {option['votes']}\n"

    def call_gpt(self, messages):
        # calling chatGPT API
        try:
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.8,
                presence_penalty=1.5,
            )
            chatgpt_reply = chat.choices[0].message["content"]
        except Exception:
            raise

        logger.info(f"{chatgpt_reply}")
        return chatgpt_reply

    def extract_question_options(self, llm_reply):
        question_matches = re.findall(self.question_regex, llm_reply)
        option_matches = re.findall(self.option_regex, llm_reply)

        # if ChatGPT gives activity then we skip this part
        if len(question_matches) > 0:
            options_list = []
            for i in range(len(option_matches)):
                # extract only the first 4 options
                if len(options_list) == 4:
                    break

                option = Option(option_id=str(i + 1), option_text=option_matches[i])
                options_list.append(option)

            question_id = sha1(question_matches[0].encode("utf-8")).hexdigest()
            question = Question(
                question_id=question_id,
                question_text=question_matches[0],
                options=options_list,
            )

            logger.info(question.to_dict())
            return question
        else:
            return None

    def extract_activities(self, llm_reply):
        # format into a json that can be emitted
        activities_matches = re.findall(self.activity_regex, llm_reply)

        activities = []

        for i in range(len(activities_matches)):
            activities.append(
                Option(option_id=str(i + 1), option_text=activities_matches[i])
            )

        return {"activities": activities, "num_of_activity": len(activities)}

    def retry_logic(self, message):
        # we retry at most 5 times.
        for i in range(5):
            retry_reply = self.call_gpt(message)
            question_and_options = self.extract_question_options(retry_reply)
            if len(question_and_options.to_dict()["options"]) >= 2:
                return question_and_options

        raise ValueError("Retry logic failed.")
