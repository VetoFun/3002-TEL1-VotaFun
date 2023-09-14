from backend.src.routes import chatgpt_blueprint
from flask import request, jsonify
import openai
import re
from hashlib import sha1

messages = [
    {
        "role": "system",
        "content": "I am planning a group activity in the west of Singapore and it will be an indoor activity. "
        "Can you ask 5 questions with 4 options to choose? After 5 questions, suggest 4 activities in "
        "Singapore that the group will enjoy, and a short description. Give each question one at a time, and "
        "generate each question based on the votes of the previous question. "
        "Format the questions in the following manner. "
        "Question <question number>: <question>"
        "A) <option A>"
        "B) <option B>"
        "C) <option C>"
        "D) <option D>"
        ""
        "Give the activities in the following format at the end of the questions. The location must be in Singapore."
        "Activity 1: <activity name>"
        "Activity 2: <activity name>"
        "Activity 3: <activity name>"
        "Activity 4: <activity name>",
    }
]


@chatgpt_blueprint.route("/chatgpt", methods=["POST"])
def chatgpt():
    """
    API which is a wrapper to call openai API. This fetches all the questions and votes so far, then uses openai
    ChatCompletion to get a reply from ChatGPT.
    :return:
    """
    # activity_regex = r'Activity.*[0-9].*'
    activity_regex = r"Activity \d+: (.+)"
    # question_regex = r'Question.*[0-9]:\s*.*'
    question_regex = r"Question \d+: (.+)"
    option_regex = r"[A-Z]\).*"

    if len(request.json) > 0:
        data = request.get_json()
        votes = {
            "role": "user",
            "content": f"A: {data['A']}, B: {data['B']}, C: {data['C']}, D: {data['D']}",
        }
        messages.append(votes)
    print(messages)
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    chatgpt_reply = chat.choices[0].message["content"]

    activity_matches = re.findall(activity_regex, chatgpt_reply)
    question_matches = re.findall(question_regex, chatgpt_reply)
    option_matches = re.findall(option_regex, chatgpt_reply)

    reply = {"role": "assistant", "content": chat.choices[0].message["content"]}
    messages.append(reply)

    rsp = {"Success": True}
    if len(activity_matches) == 0:
        rsp["Question"] = question_matches[0]
        rsp["QuestionID"] = sha1(rsp["Question"].encode("utf-8")).hexdigest()
        rsp["num_of_options"] = len(option_matches)
        rsp["Options"] = {}

        for i in option_matches:
            text = i.split(") ")
            rsp["Options"][text[0]] = text[1]
    else:
        rsp["num_of_activity"] = len(activity_matches)
        rsp["Activities"] = {}
        for i in range(len(activity_matches)):
            rsp["Activities"][f"Activity: {i + 1}"] = activity_matches[i]
    return jsonify(rsp), 200
