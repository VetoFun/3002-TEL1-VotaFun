from flask import Flask, jsonify, request, json
from redisdb.src.Database import Database
from datetime import datetime
from hashlib import sha1
import openai
from dotenv import load_dotenv
import os
import uuid
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
load_dotenv(".env")
# database setup
redis_database = Database()
# openai setup
openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
    {
        "role": "system",
        "content": """I am planning a group activity in the west of Singapore and it will be an indoor activity. Can you ask 5 questions with 4 options to choose? After 5 questions, suggest 4 activities in Singapore that the group will enjoy, and a short description. Give each question one at a time, and generate each question based on the votes of the previous question. 
            Format the questions in the following manner. 
            Question <question number>: <question>
            A) <option A>
            B) <option B>
            C) <option C>
            D) <option D>

            Give the activities in the following format at the end of the questions. The location must be in Singapore.
            Activity 1: <activity name>
            Activity 2: <activity name>
            Activity 3: <activity name>
            Activity 4: <activity name>"""
    }
]

@app.route('/rooms', methods=['POST'])
def create_room():
    """
    An entry will be created in the database for the created room. A room code will be generated for the room. Set last_activity time in room.
    :return: JSON object
    """
    data = request.get_json()
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    room_code = sha1(timestamp.encode("utf-8")).hexdigest()
    room_id = uuid.uuid4().hex
    room_json = {
        "roomid": room_id,
        "roomcode": room_code,
        "hostid": data['Userid'],
        "numuser": 30,
        "current_user": 1,
        "status": "Waiting",
        "last_activity": timestamp,
        "roomlocation": data['Location'],
        "roomactivity": data['Activity'],
        "users": [{
            "userid": data['Userid'],
            "username": data['Username']
        }],
        "questions": []
    }
    # return "Internal server error", 500
    information = {
        "Success": True,
        "Room code": room_code,
        "Room id": room_id
    }
    return jsonify(information), 200


@app.route('/rooms/<roomid>', methods=['DELETE'])
def delete_room(roomid):
    """
    Remove the database entry for the room. Entries in the database for the room’s users, questions, votes, and options will be removed.
    :return: None
    """
    # success = database.remove(roomid)
    # if (success):
    # return jsonify({
    #   "Success" = True
    # }), 200
    # return "Internal server error", 500


@app.route('/rooms', methods=['GET'])
def get_room_id():
    """
    Finds the roomid corresponding to the room code. If room does not exist, return False.
    :return: None
    """
    roomcode = request.args['roomcode']
    return "Success", 200
    # database can create an index on roomcode -> maps to roomid


@app.route('/rooms/<roomid>/users', methods=['POST'])
def join_room(roomid):
    """
    Checks the num_users, and adds user to users table if number is < capacity. Increment num_users by 1 and set last_activity time in room.
    :return: None
    """
    print(roomid)
    return "Success",200
    # database can create an index on roomcode -> maps to roomid


@app.route('/rooms/<roomid>/users/<userid>', methods=['DELETE'])
def leave_room(roomid, userid):
    """
    A user clicks “leave room”. Remove user from database and reduce num_users by 1.
    :return: None
    """
    print(roomid, userid)
    return "Success", 200


@app.route('/rooms/<roomid>/users', methods=['GET'])
def get_all_users():
    """
    Get all users in a room
    :return: None
    """


@app.route('/rooms/<roomid>/changehost', methods=['PUT'])
def change_host():
    """
    Changes the host into another user.
    :return: None
    """


@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    """
    API which is a wrapper to call openai API. This fetches all the questions and votes so far, then uses openai
    ChatCompletion to get a reply from ChatGPT.
    :return:
    """
    activity_regex = r'Activity.*[0-9].*'
    question_regex = r'Question.*[0-9]:\s*.*'
    option_regex = r'[A-D]\).*'

    if len(request.json) > 0:
        data = request.get_json()
        votes = {
            "role": "user",
            "content": f"A: {data['A']}, B: {data['B']}, C: {data['C']}, D: {data['D']}"
        }
        messages.append(votes)
    print(messages)
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    chatgpt_reply = chat.choices[0].message["content"]

    activity_matches = re.findall(activity_regex, chatgpt_reply)
    question_matches = re.findall(question_regex, chatgpt_reply)
    option_matches = re.findall(option_regex, chatgpt_reply)

    reply = {
        "role": "assistant",
        "content": chat.choices[0].message["content"]
    }
    messages.append(reply)

    rsp = {
        "Success": True
    }
    if len(activity_matches) == 0:
        rsp["Question"] = question_matches[0].split(": ")[1]
        rsp["QuestionID"] = sha1(rsp["Question"].encode("utf-8")).hexdigest()
        rsp["num_of_options"] = len(option_matches)
        rsp["Options"] = {}

        for i in option_matches:
            text = i.split(') ')
            rsp["Options"][text[0]] = text[1]
    else:
        rsp["num_of_activity"] = len(activity_matches)
        rsp["Activities"] = {}
        for i in activity_matches:
            text = i.split(':')
            rsp["Activities"][text[0]] = text[1]
    return jsonify(rsp), 200


if __name__ == "__main__":
    app.run(debug=True)
