import redis
import json
from room_class import Room
from question_class import Question
from user_class import User
from option_class import Option
from typing import List, Dict, Union, Optional


def get_room_key(room_id: str) -> str:
    """
    Get the Redis key for a room based on its ID.

    Args:
        room_id (str): The unique identifier of the room.

    Returns:
        str: The Redis key for the room.
    """
    return f"room_id:{room_id}"


class Database:
    def __init__(self):
        """
        Represents a Redis database for managing room data.

        Attributes:
            connection (redis.Redis): The Redis database connection.
            room_ids (dict): A dictionary to store room IDs and
            corresponding room codes.
            roomcode_to_roomid_index (dict): A dictionary to index room
            codes to room IDs.
        """
        self.connection = redis.Redis(host="localhost", port=6379)
        self.room_ids = {}
        self.roomcode_to_roomid_index = {}

    def does_room_id_exist(self, room_id: str) -> bool:
        """
        Check if a room ID exists in the database.

        Args:
            room_id (str): The room ID to check.

        Returns:
            bool: True if the room ID exists, False otherwise.
        """
        if room_id in self.room_ids:
            return True
        else:
            return False

    def query(
        self, room_id: str
    ) -> Optional[Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]]:
        """
        Query room data from the database.

        Args:
            room_id (str): The room ID to retrieve data for.

        Returns:
            dict or None: A dictionary representing room data or None if data
            is not found.
        """
        room_key = get_room_key(room_id)
        if self.does_room_id_exist(room_id):
            room_data_str = self.connection.hget(room_key, "room_data")
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
                # Handle case where the field does not exist or has a None
                # value
                print(f"Error: {room_key} does not exist.")
                return None
        else:
            print(f"Error: {room_key} does not exist.")

    def store(self, room_id: str, room_code: str, data: dict) -> bool:
        """
        Store room data in the database.

        Args:
            room_id (str): The room ID to store data for.
            room_code (str): The room code or name.
            data (dict): The data to store in the room.

        Returns:
            bool: True if data is successfully stored, False otherwise.
        """
        # Check if the 'room_id' already exists in Redis
        if self.does_room_id_exist(room_id):
            print(f"Error: {get_room_key(room_id)} already exists.")
            return False
        else:
            # Add the room ID to the dictionary
            self.room_ids[room_id] = room_code
            self.roomcode_to_roomid_index[room_code] = room_id
            room_key = get_room_key(room_id)
            # Store room data in Redis Hash
            self.connection.hset(room_key, "room_data", json.dumps(data))
            print(f"{get_room_key(room_id)} successfully stored.")
            return True

    def remove(self, room_id: str) -> bool:
        """
        Remove room data from the database.

        Args:
            room_id (str): The room ID to remove data for.

        Returns:
            bool: True if data is successfully removed, False otherwise.
        """
        if self.does_room_id_exist(room_id):
            room_key = get_room_key(room_id)
            self.connection.delete(room_key)
            print(f"{get_room_key(room_id)} removed successfully from Redis.")
            return True
        else:
            print(f"Error: {get_room_key(room_id)} does not exist.")
            return False

    def get_users(self, room_id: str) -> List[Dict[str, str]]:
        """
        Get a list of users in a room from the database.

        Args:
            room_id (str): The room ID to retrieve user data for.

        Returns:
            list: A list of dictionaries representing users.
        """
        room_data = self.query(room_id)
        users = room_data.get("users", [])
        return users

    def get_questions(
        self, room_id: str
    ) -> List[Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]]:
        """
        Get a list of questions in a room from the database.

        Args:
            room_id (str): The room ID to retrieve question data for.

        Returns:
            list: A list of dictionaries representing questions.
        """
        room_data = self.query(room_id)
        questions = room_data.get("questions", [])
        return questions

    def insert_questions(self, room_id: str, new_question: Question) -> bool:
        """
        Insert a new question into a room in the database.

        Args:
            room_id (str): The room ID to insert the question into.
            new_question (dict): The new question data.

        Returns:
            bool: True if the question is successfully inserted,
            False otherwise.
        """
        room_key = get_room_key(room_id)
        room_data = self.query(room_id)
        room_data["questions"].append(new_question.to_dict())
        # Update the Redis Hash with the modified data
        if self.connection.hset(room_key, "room_data", json.dumps(room_data)):
            print(
                f"New question: {new_question['question_id']} was "
                f"successfully inserted in Room: {room_id}"
            )
            return True
        else:
            print("Error in adding question")
            return False

    def query_all_hash_keys(self):
        """
        Query all hash keys in the Redis database and print field-value pairs.
        """
        hash_keys = self.connection.keys("room_id:*")
        print("hash_keys:", hash_keys)
        for key in hash_keys:
            field_value_pairs = self.connection.hgetall(key)
            print(f"Hash Key: {key}")
            print("Field-Value Pairs:")
            for field, value in field_value_pairs.items():
                print(f"{field}: {value}")


if __name__ == "__main__":
    # Example usage:
    # Create a room, add users, questions, and options
    room = Room(
        room_id="r1",
        room_code="AAAA",
        number_of_user=2,
        max_capacity=5,
        last_activity="2023-09-13 10:00:00",
        host_id="123",
        status="waiting",
        room_location="idkwhatisthis",
        room_activity="idkwhatisthis",
    )
    room.add_user(User("u1", "Alice"))
    room.add_user(User("u2", "Bob"))
    question1 = Question(
        question_id="q1", question_text="What's your " "favorite color?"
    )
    question1.add_option(Option(option_id="o1", option_text="Red", current_votes=3))
    question1.add_option(Option(option_id="o2", option_text="Blue", current_votes=5))
    room.add_question(question1)

    room2 = Room(
        room_id="r2",
        room_code="BBBB",
        number_of_user=2,
        max_capacity=5,
        last_activity="2023-09-13 10:00:00",
        host_id="123",
        status="waiting",
        room_location="idkwhatisthis",
        room_activity="idkwhatisthis",
    )
    room2.add_user(User("u1", "Alice"))
    room2.add_user(User("u2", "Bob"))
    question1 = Question(
        question_id="q1", question_text="What's your " "favorite color?"
    )
    question1.add_option(Option(option_id="o1", option_text="Red", current_votes=3))
    question1.add_option(Option(option_id="o2", option_text="Blue", current_votes=5))
    room2.add_question(question1)

    test_db = Database()
    # Test for store function
    test_db.store(room_id=room.room_id, room_code=room.room_code, data=room.to_dict())
    test_db.store(
        room_id=room2.room_id, room_code=room2.room_code, data=room2.to_dict()
    )
    # Test for duplicate checking
    test_db.store(
        room_id=room2.room_id, room_code=room2.room_code, data=room2.to_dict()
    )
    # Test for query function
    print("Querying test:", test_db.query(room.room_id))
    # Test for get_user function (User Info retrieval)
    print("users:", test_db.get_users(room_id=room2.room_id))
    # Test for get_question function (Question Info retrieval)
    print("questions:", test_db.get_questions(room_id=room2.room_id))
    # Test for insert_question function
    question2 = Question(
        question_id="q2", question_text="What's is your favorite monster?"
    )
    question2.add_option(Option(option_id="o1", option_text="Ant", current_votes=5))
    question2.add_option(Option(option_id="o2", option_text="Dog", current_votes=1))
    test_db.insert_questions(room2.room_id, question2)
    print("Querying test:", test_db.query("r2"))
