import openai
import re
from hashlib import sha1


def chatgpt_func(data, database):
    room_id = data["roomid"]

    # get the room dictionary
    try:
        room = database.query_room_data(room_id, True)
        room_location = room["room_location"]
        room_activity = room["room_activity"]
    except KeyError:
        return None

    # initial prompt
    messages = [
        {
            "role": "system",
            "content": f"I am planning a group activity in the {room_location} of Singapore and it will be an "
            f"{room_activity} activity. Can you ask 5 questions with 4 options to choose? After 5 questions,"
            f" suggest 4 activities in Singapore that the group will enjoy, and a short description. "
            f"Give each question one at a time, and generate each question based on the votes of the "
            f"previous question. "
            "Format the questions in the following manner. "
            "Question <question number>: <question>"
            "A) <option A>"
            "B) <option B>"
            "C) <option C>"
            "D) <option D>"
            ""
            "Give the activities in the following format at the end of the questions. "
            "The location must be in Singapore."
            "Activity 1: <activity name>"
            "Activity 2: <activity name>"
            "Activity 3: <activity name>"
            "Activity 4: <activity name>",
        }
    ]

    # regexes to extract information Chatgpt returns
    activity_regex = r"Activity \d+: (.+)"
    question_regex = r"Question \d+: (.+)"
    option_regex = r"[A-Z]\).*"

    past_questions = room["questions"]
    for i in range(0, len(past_questions)):
        questions = {"role": "assistant", "content": past_questions[i]["question_text"]}
        messages.append(questions)

        if i + 1 != len(past_questions):
            votes = past_questions[i]["options"]

            content = ""
            for key, value in votes.items():
                content += f"{key}: value, "

            votes_question = {
                "role": "user",
                "content": content[:-2],
            }
            messages.append(votes_question)

    if "num_of_votes" in data:
        content = ""
        for i in range(0, data["num_of_votes"]):
            content += f"{chr(65 + i)}: {data['votes'][chr(65 + i)]}, "

        votes = {
            "role": "user",
            "content": content,
        }
        messages.append(votes)

    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    chatgpt_reply = chat.choices[0].message["content"]

    activity_matches = re.findall(activity_regex, chatgpt_reply)
    question_matches = re.findall(question_regex, chatgpt_reply)
    option_matches = re.findall(option_regex, chatgpt_reply)

    reply = {"role": "assistant", "content": chat.choices[0].message["content"]}
    messages.append(reply)
    print(messages)
    rsp = {"success": True}
    if len(activity_matches) == 0:
        rsp["question"] = question_matches[0]
        rsp["QuestionID"] = sha1(rsp["question"].encode("utf-8")).hexdigest()
        rsp["num_of_options"] = len(option_matches)
        rsp["Options"] = {}
        database.add_question(room_id, rsp["QuestionID"], rsp["question"])

        for i in option_matches:
            text = i.split(") ")
            rsp["Options"][text[0]] = text[1]
            database.add_option(room_id, rsp["QuestionID"], text[0], text[1])

    else:
        rsp["num_of_activity"] = len(activity_matches)
        rsp["Activities"] = {}
        for i in range(len(activity_matches)):
            rsp["Activities"][f"Activity: {i + 1}"] = activity_matches[i]

    return rsp
