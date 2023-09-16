import openai
import re
from hashlib import sha1
from src.logger import logger


def chatgpt_func(data, database):
    room_id = data["room_id"]

    # get the room dictionary
    try:
        room = database.query_room_data(room_id, True)
        room_location = room["room_location"]
        room_activity = room["room_activity"]
    except KeyError:
        return {"success": False, "error": "Internal Server Error"}

    # initial prompt
    messages = [
        {
            "role": "system",
            "content": f"We are a group of friends and you play the role of a mind reader. We are thinking of doing"
            f"an {room_activity} in {room_location} Singapore. Since you are a mind reader, guess what"
            f"activity we are thinking of doing. \n"
            f"Here is how you can generate questions and votes. Questions are generated based on the "
            f"previous questions and votes. Options for the current question is based on the question. "
            f"Following this format ensures that you will be able to guess what we are thinking of doing. "
            f"The rule is that you can only ask 5 questions with 4 options to choose from. "
            f"Give one question each time, generating questions and options based on the previous "
            f"questions and votes.\n"
            f"Always format questions and options like this: "
            f"Question <x>: <question>\n"
            f"<A>) <option A>\n"
            f"<B>) <option B>\n"
            f"<C>) <option C>\n"
            f"<D>) <option D>\n"
            f"After 5 questions, suggest 4 {room_activity} activities that we are thinking of doing in "
            f"{room_location} Singapore in this format:"
            f"Activity <x>: <activity>\n"
            f"Suggest activities only after question 5 based on the all questions asked and the votes for "
            f"each option. Do not repeat questions and votes. Ask questions normally, like a conversation."
            f"Do not give open-ended questions, only multiple choice."
            f"Options given must be based on the question.",
        }
    ]

    # regexes to extract information Chatgpt returns
    activity_regex = r"Activity \d+: (.+)"
    question_regex = r"Question \d+: (.+)"
    option_regex = r".*[A-Z].*\).*"

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
                    content += f"{option['option_id']}: {option['votes']}\n"

                votes_question = {
                    "role": "user",
                    "content": content[:-1],
                }
                messages.append(votes_question)

    if "num_of_votes" in data:
        content = ""
        for i in range(0, data["num_of_votes"]):
            content += f"{chr(65 + i)}) {data['votes'][chr(65 + i)]}\n"

            # update votes in question
            database.set_vote(
                room_id, data["question_id"], chr(65 + i), data["votes"][chr(65 + i)]
            )
        votes = {
            "role": "user",
            "content": content
            + "Remember you can only ask 5 questions for us, and only give the activity we are"
            "thinking of after question number 5. Give properly formatted questions with "
            "4 valid options to choose. We will not tell you anything if you do not give us "
            "valid options A to D to choose from. \n"
            "The format is:"
            "Question <x>: <question>\n"
            "<A>) <option A>\n"
            "<B>) <option B>\n"
            "<C>) <option C>\n"
            "<D>) <option D>\n"
            "Do not repeat or ask similar questions with their options."
            "Do not give open-ended questions, only multiple choice with options to choose."
            "Options given must be based on the question.",
        }
        messages.append(votes)

    # calling chatGPT API
    try:
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        chatgpt_reply = chat.choices[0].message["content"]
    except Exception:
        return {"success": False, "error": "Internal Server Error"}

    logger.info(f"{chatgpt_reply}")

    # use regexes to filter out the information we need
    activity_matches = re.findall(activity_regex, chatgpt_reply)
    question_matches = re.findall(question_regex, chatgpt_reply)
    option_matches = re.findall(option_regex, chatgpt_reply)

    reply = {"role": "assistant", "content": chat.choices[0].message["content"]}
    messages.append(reply)
    logger.info(f"{messages}")

    rsp = {"success": True}
    # if chatGPT ask a question
    if len(activity_matches) == 0:
        rsp["question"] = question_matches[0]
        rsp["question_id"] = sha1(rsp["question"].encode("utf-8")).hexdigest()
        rsp["num_of_options"] = len(option_matches)
        rsp["options"] = {}

        # store question in database
        database.add_question(room_id, rsp["question_id"], rsp["question"])

        for i in option_matches:
            option_extraction_regex = r"\s[A-Za-z].*"
            option_id_extraction_regex = r"[A-Z]"
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
