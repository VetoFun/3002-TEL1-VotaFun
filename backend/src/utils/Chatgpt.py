import openai
import re
from hashlib import sha1
from src.logger import logger


def chatgpt_func(data, database):
    """
    Calls OpenAI API to get questions and recommended activities. Stores the previous votes into the database, and
    returns a JSON with the current question and options.
    :param data: JSON of the request body.
    :param database: Application database.
    :return: JSON with "success" == True, and the questions and options if success,
    otherwise "success" == False with an error is returned.
    """
    room_id = data["room_id"]

    # get the room dictionary
    try:
        room = database.query_room_data(room_id, True)
        room_location = room["room_location"]
        room_activity = room["room_activity"]
    except KeyError:
        raise

    # initial prompt
    messages = [
        {
            "role": "system",
            "content": f"We are planning a {room_activity} in {room_location} Singapore and will need your help. "
            f"Can you give us 5 questions one at a time, along with 4 options to vote for. Questions and "
            f"votes must be generated based on the previous response except for the first question."
            f"After getting votes for the 5 "
            f"questions, suggest 4 {room_activity} for us to do. Only give the activity after all voting is "
            f"done.\n"
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
            f"After 5 questions, based on the votes suggest 4 {room_activity} activity in {room_location} Singapore "
            f"using this format.\n"
            f"Activity x: <activity name>\n"
            f"You do not need to show the votes at the end. Only suggest 4 activities after question 5. The 4 activity "
            f"suggested must be in Singapore and only show me the suggested activities.",
        }
    ]

    # regexes to extract information Chatgpt returns
    activity_regex = r"Activity \d+: (.+)"
    question_regex = r"Question \d+: (.+)"
    option_regex = r"[0-9]\).*"

    # adding the past questions asked by chatGPT and their votes
    past_questions = room["questions"]
    if len(past_questions) != 0:
        for i in range(0, len(past_questions)):
            questions = {
                "role": "assistant",
                "content": f"Question {i+1}: " + past_questions[i]["question_text"],
            }
            messages.append(questions)

            if i + 1 != len(past_questions):
                votes = past_questions[i]["options"]

                content = ""
                for option in votes:
                    content += f"{option['option_text']}: {option['votes']}\n"

                votes_question = {
                    "role": "user",
                    "content": content[:-1],
                }
                messages.append(votes_question)

    if "num_of_votes" in data:
        content = ""
        # get the last question asked
        last_question = past_questions[-1]
        for i in range(0, data["num_of_votes"]):
            # content += f"{chr(65 + i)}) {data['votes'][chr(65 + i)]}\n"
            content += f"{last_question['options'][i]['option_text']}: {data['votes'][str(i + 1)]}\n"

            # update votes in question
            database.set_vote(
                # room_id, data["question_id"], chr(65 + i), data["votes"][chr(65 + i)]
                room_id,
                data["question_id"],
                str(i + 1),
                data["votes"][str(i + 1)],
            )
        votes = {
            "role": "user",
            "content": content
            + "We are indecisive so give us a properly formatted question "
            "with 4 options to vote. Remember do not repeat or ask similar questions and options. "
            "Suggest 4 activities after question 5 and stop asking questions and options."
            "Format the questions in this manner: \n"
            "Question <x>: <question>\n"
            "1) <option 1>\n"
            "2) <option 2>\n"
            "3) <option 3>\n"
            "4) <option 4>\n",
        }
        messages.append(votes)

    # calling chatGPT API
    try:
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        chatgpt_reply = chat.choices[0].message["content"]
    except Exception:
        raise

    logger.info(f"{chatgpt_reply}")

    # use regexes to filter out the information we need
    activity_matches = re.findall(activity_regex, chatgpt_reply)
    question_matches = re.findall(question_regex, chatgpt_reply)
    option_matches = re.findall(option_regex, chatgpt_reply)

    # reply = {"role": "assistant", "content": chat.choices[0].message["content"]}
    # messages.append(reply)
    logger.info(f"{messages}")

    rsp = {"success": True}
    # if chatGPT ask a question
    if len(question_matches) != 0:
        rsp["question"] = question_matches[0]
        rsp["question_id"] = sha1(rsp["question"].encode("utf-8")).hexdigest()
        rsp["num_of_options"] = len(option_matches)
        rsp["options"] = {}

        # store question in database
        database.add_question(room_id, rsp["question_id"], rsp["question"])

        for i in option_matches:
            option_extraction_regex = r"(?<= )[0-9A-Za-z].*"
            option_id_extraction_regex = r"[0-9]"
            option = re.search(option_extraction_regex, i).group(0)
            option_id = re.search(option_id_extraction_regex, i).group(0)

            rsp["options"][option_id] = option
            # store options in database
            database.add_option(room_id, rsp["question_id"], option_id, option)
    # end of the 5th question
    else:
        rsp["num_of_activity"] = len(activity_matches)
        rsp["activities"] = {}
        for i in range(len(activity_matches)):
            rsp["activities"][f"activity: {i + 1}"] = activity_matches[i]

    return rsp
