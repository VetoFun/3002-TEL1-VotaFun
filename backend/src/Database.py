import redis, json

option1 = {
    'option_id': '1',
    'option_text': 'Option 1',
    'current_votes': 0
}
option2 = {
    'option_id': '2',
    'option_text': 'Option 2',
    'current_votes': 0
}
question1 = {
    'question_id': 'q1',
    'question_text': 'What is your favorite color?',
    'options': [option1, option2]
}
question2 = {
    'question_id': 'q2',
    'question_text': 'Which programming language do you prefer?',
    'options': [option1, option2]
}
user1 = {
    'user_id': 'u1',
    'user_name': 'Alice'
}
user2 = {
    'user_id': 'u2',
    'user_name': 'Bob'
}
room1 = {
    'room_id': 'r1',
    'room_code': 'AZYC',
    'number_of_user': 2,
    'max_capacity': 5,
    'last_activity': '2023-09-13 10:00:00',
    'questions': [question1, question2],
    'host_id': 'u1',
    'status': 'active',
    'roomlocation': 'Living room',
    'roomactivity': 'Discussion',
    'users': [user1, user2]
}
test_data = room1

class Database:
    def __init__(self):
        self.connection = redis.Redis(host='localhost', port=6379)
        self.room_ids = {}
        self.roomcode_to_roomid_index = {}
    def check_if_room_exists(self, room_id):
        if room_id in self.room_ids:
            return True
        else:
            return False
    def query(self, room_id):
        if self.check_if_room_exists(room_id):
            room_key = f'room_id:{room_id}'
            room_data_str = self.connection.hget(room_key, 'room_data')
            # Check if the field exists and the value is not None
            if room_data_str is not None:
                try:
                    room_data = json.loads(room_data_str)
                    return room_data
                except json.JSONDecodeError:
                    # Handle JSON parsing error
                    print(f"Error: Invalid JSON data for room {room_id}")
                    return None
            else:
                # Handle case where the field does not exist or has a None value
                print(f"Error: Room {room_id} does not exist or has no 'room_data' field.")
                return None
        else:
            print(f"Error: Room {room_id} does not exist.")


    def store(self, room_id, room_code, data):
        # Check if the 'room_id' already exists in Redis
        if self.check_if_room_exists(room_id):
            print(f"Error: Room {room_id} already exists.")
        else:
            # Add the room ID to the dictionary
            self.room_ids[room_id] = room_code
            self.roomcode_to_roomid_index[room_code] = room_id
            room_key = f'room_id:{room_id}'
            # Store room data in Redis Hash
            self.connection.hset(room_key, 'room_data', json.dumps(data))
            print(f"{room_id} successfully stored.")

    def remove(self, room_id):
        if self.check_if_room_exists(room_id):
            room_key = f'room_id:{room_id}'
            self.connection.delete(room_key)
            print(f"Room {room_id} removed successfully from Redis.")
            return self.roomcode_to_roomid_index.pop(self.room_ids.pop(room_id))
        else:
            print(f"Error: Room {room_id} does not exist in Redis.")

    def get_users(self, room_id):
        room_data = self.query(room_id)
        users = room_data.get('users', [])
        return users
    def get_questions(self, room_id):
        room_data = self.query(room_id)
        questions = room_data.get('questions', [])
        return questions

    def insert_questions(self, room_id, new_question):
        room_key = f'room_id:{room_id}'
        room_data = self.query(room_id)
        room_data['questions'].append(new_question)
        # Update the Redis Hash with the modified data
        self.connection.hset(room_key, 'room_data', json.dumps(room_data))
        print(f"New question: {new_question['question_id']} was successfully inserted in Room: {room_id}")
    def query_all_hash_keys(self):
        hash_keys = self.connection.keys("room_id:*")
        print("hash_keys:", hash_keys)
        for key in hash_keys:
            field_value_pairs = self.connection.hgetall(key)
            print(f"Hash Key: {key}")
            print("Field-Value Pairs:")
            for field, value in field_value_pairs.items():
                print(f"{field}: {value}")


test_db = Database()
# Test for store function
test_db.store(room_id='r1', room_code='AAAA', data=test_data)
test_db.store(room_id='r2', room_code='BBBB', data=test_data)
# Test for duplicate checking
test_db.store(room_id='r2', room_code='BBBB', data=test_data)
# Test for query function
print("Querying test:", test_db.query('r1'))
# Test for get_user function (User Info retrieval)
print("users:", test_db.get_users(room_id='r2'))
# Test for get_question function (Question Info retrieval)
print("questions:", test_db.get_questions(room_id='r2'))
# Test for insert_question function
question3 = {
    'question_id': 'q3',
    'question_text': 'What is your favorite monster?',
    'options': [option1, option2]
}
test_db.insert_questions('r2', question3)
print("Querying test:", test_db.query('r2'))
# Test for get_user function (User Info retrieval)