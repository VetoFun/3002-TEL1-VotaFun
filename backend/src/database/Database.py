import datetime
import logging
import redis
import json
from src.database.Room import Room
from src.database.Question import Question
from src.database.User import User
from src.database.Option import Option
from typing import List, Dict, Union, Optional

# Define a logger for your class
logger = logging.getLogger(__name__)


def get_room_key(room_id: str) -> str:
    """
    Get the Redis key for a room based on its ID.

    Args:
        room_id (str): The unique identifier of the room.

    Returns:
        str: The Redis key for the room.
    """
    # Can add things to be more secure. But will need to have a "decode_room_key" when using "query_all_hash_key"
    # function
    return f"{room_id}"


class Database:
    def __init__(self, redis_url: str = "redis://localhost:6379") -> None:
        """
        Represents a Redis database for managing room data.

        Args:
            redis_url (str): The URL used to connect to the Redis server.

        Attributes:
            r (redis.from_url): The Redis database connection.
            roomcode_to_roomid_index (dict): A dictionary for indexing room
                codes to room IDs.
        """
        self.r = redis.from_url(redis_url)
        self.roomcode_to_roomid_index = {}

    def does_room_id_exist(self, room_id: str) -> bool:
        """
        Check if a room ID exists in the database.

        Args:
            room_id (str): The room ID to check.

        Returns:
            bool: True if the room ID exists, False otherwise.
        """
        if self.r.keys(room_id):
            return True
        else:
            return False

    def query_room_data(
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
        if self.does_room_id_exist(room_id):
            room_data_byte = self.r.hgetall(room_id)
            # Check if the field exists and the value is not None
            if room_data_byte is not None:
                try:
                    room_data = {}
                    for key, value in room_data_byte.items():
                        room_data[key.decode("utf-8")] = value.decode("utf-8")
                    return Room.from_dict(room_data)
                except json.JSONDecodeError:
                    # Handle JSON parsing error
                    logger.error(f"Error: Invalid JSON data for room {room_id}")
                    return None
            else:
                # Handle case where the field does not exist or has a None
                # value
                logger.error(f"Error: {room_id}'s data does not exist.")
                return None
        else:
            logger.error(f"Error: {room_id} does not exist.")

    def _query_single_field(
        self, room_id: str, field: str
    ) -> Optional[Union[Dict, None]]:
        """
        Query a single field from room data in the database.

        Note: Not meant to be called from outside. Use 'get_users', 'get_options', 'get_vote', etc. function instead.

        Args:
            room_id (str): The room ID to retrieve data for.
            field (str): The field name to retrieve.

        Returns:
            dict or None: A dictionary representing the field data or None if data is not found.
        """
        if self.does_room_id_exist(room_id):
            db_data = json.loads(self.r.hget(room_id, field).decode("utf-8"))
            logger.info(f"db_data's {field} was successfully retrieved from {room_id}")
            return db_data
        else:
            logger.error(f"Unable to find {room_id}, can't retrieve {field}'s data.")
            return None

    def store_room_data(self, room_id: str, room_code: str, room_data: Room) -> bool:
        """
        Store room data in the database.

        Args:
            room_id (str): The room ID to store data for.
            room_code (str): The room code or name.
            room_data (Room): The Room object data to store in the room.

        Returns:
            bool: True if data is successfully stored, False otherwise.
        """
        # Check if the 'room_id' already exists in Redis
        if self.does_room_id_exist(room_id):
            logger.error(f"Error: {room_id} already exists.")
            return False
        else:
            self.roomcode_to_roomid_index[room_code] = room_id
            # Store room data in Redis Hash
            for key, value in room_data.to_dict().items():
                self.r.hset(room_id, key, json.dumps(value))
            logger.info(f"{room_id} successfully stored.")
            return True

    def store_single_field(self, room_id: str, field: str, data, replace: bool) -> bool:
        """
        Store a single field in room data in the database.

        Args:
            room_id (str): The room ID to store data for.
            field (str): The field name to store.
            data: The data to store in the field.
            replace (bool): Whether to replace the existing data or append it.

        Returns:
            bool: True if data is successfully stored, False otherwise.
        """
        db_data = json.loads(self.r.hget(room_id, field).decode("utf-8"))
        # Check if 'data' has a .to_dict() method
        if hasattr(data, "to_dict") and callable(data.to_dict):
            if replace:
                db_data = data.to_dict()
            else:
                db_data.append(data.to_dict())
        else:
            if replace:
                db_data = data
            else:
                db_data.append(data)

        if self.does_room_id_exist(room_id):
            self.r.hset(room_id, field, json.dumps(db_data))
            logger.info(f"{field}: {data} was successfully inserted in Room: {room_id}")
            return True
        else:
            logger.error(f"Unable to find {room_id}, can't add {field}: {data}.")
            return False

    def remove_room_data(self, room_id: str) -> bool:
        """
        Remove room data from the database.

        Args:
            room_id (str): The room ID to remove data for.

        Returns:
            bool: True if data is successfully removed, False otherwise.
        """
        if self.does_room_id_exist(room_id):
            room_key = room_id
            self.r.delete(room_key)
            logger.info(f"{room_id} removed successfully from Redis.")
            return True
        else:
            logger.error(f"Error: {room_id} does not exist.")
            return False

    def get_users(self, room_id: str) -> List[Dict[str, str]]:
        """
        Get a list of users in a room from the database.

        Args:
            room_id (str): The room ID to retrieve user data for.

        Returns:
            list: A list of dictionaries representing users.
        """
        return self._query_single_field(room_id=room_id, field="users")

    def insert_users(self, room_id: str, new_user: User) -> bool:
        """
        Insert a new user into a room in the database.

        Args:
            room_id (str): The room ID to insert the question into.
            new_user (User): The new question data.

        Returns:
            bool: True if the question is successfully inserted, False otherwise.
        """
        if self.store_single_field(
            room_id=room_id, field="users", data=new_user, replace=False
        ):
            return True
        else:
            return False

    def remove_users(self, room_id: str, user_id: str) -> bool:
        """
        Insert a new user into a room in the database.

        Args:
            room_id (str): The room ID to insert the question into.
            user_id (User): The user_id to be removed

        Returns:
            bool: True if the user is successfully removed, False otherwise.
        """
        users = self.get_users(room_id=room_id)
        if type(users) is dict:
            users = [users]
        for user in users:
            if user_id == user["user_id"]:
                users.remove(user)
                logger.info(
                    f"User with user_id: {user_id} was successfully removed from {room_id}"
                )

        if self.store_single_field(
            room_id=room_id, field="users", data=users, replace=True
        ):
            return True
        else:
            return False

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
        return self._query_single_field(room_id=room_id, field="questions")

    def insert_question(self, room_id: str, new_question: Question) -> bool:
        """
        Insert a new question into a room in the database.

        Args:
            room_id (str): The room ID to insert the question into.
            new_question (dict): The new question data.

        Returns:
            bool: True if the question is successfully inserted, False otherwise.
        """
        if self.store_single_field(
            room_id=room_id, field="questions", data=new_question, replace=False
        ):
            return True
        else:
            return False

    def get_options(self, room_id: str, question_id: str) -> List[Dict]:
        """
        Get a list of options in a question from the database.

        Args:
            room_id (str): The room ID to retrieve question data for.
            question_id (str): The question ID to retrieve option data for.

        Returns:
            list: A list of dictionaries representing options.
        """
        list_of_questions = self._query_single_field(room_id=room_id, field="questions")
        for question in list_of_questions:
            if question["question_id"] == question_id:
                return question["options"]

    def update_options(
        self, room_id: str, question_id: str, data: Union[Option, List[Option]]
    ) -> bool:
        """
        Update the options in a question from the database.

        Args:
            room_id (str): The room ID to retrieve question data for.
            question_id (str): The question ID to retrieve option data for.
            data (Union[Option, List[Option]]): The option data to update.
                This can be a single Option object or a list of Option objects.

        Returns:
            bool: True if the options are successfully updated, False otherwise.
        """
        if not isinstance(data, list):
            data = [data]  # Convert a single Option object into a list if needed

        question_db = self.get_questions(room_id=room_id)
        for question in question_db:
            if question["question_id"] == question_id:
                question["options"] = [option.to_dict() for option in data]

        if self.store_single_field(
            room_id=room_id, field="questions", data=question_db, replace=True
        ):
            return True
        else:
            return False

    def get_vote(self, room_id: str, question_id: str, option_id: str):
        """
        Get the number of votes from an option from the database.

        Args:
            room_id (str): The room ID to retrieve the room data.
            question_id (str): The question ID to retrieve the question data.
            option_id (str): The option ID to retrieve the option data.

        Returns:
            int: The vote count.
        """
        list_of_questions = self._query_single_field(room_id=room_id, field="questions")
        for question in list_of_questions:
            if question["question_id"] == question_id:
                for option in question["options"]:
                    if option["option_id"] == option_id:
                        return option["votes"]

    def increment_vote(self, room_id: str, question_id: str, option_id: str) -> bool:
        """
        Increase the vote count by 1 of a Option object in the database.

        Args:
            room_id (str): The room ID to insert the question into.
            question_id (str): The question object id.
            option_id (str): The option object id.

        Returns:
            bool: True if the question is successfully inserted, False otherwise.
        """
        list_of_questions = self.get_questions(room_id=room_id)
        for question in list_of_questions:
            if question["question_id"] == question_id:
                for option in question["options"]:
                    if option["option_id"] == option_id:
                        option["votes"] += 1

        if self.store_single_field(
            room_id=room_id, field="questions", data=list_of_questions, replace=True
        ):
            return True
        else:
            return False

    def decrement_vote(self, room_id: str, question_id: str, option_id: str) -> bool:
        """
        Decrease the vote count by 1 of a Option object in the database.

        Args:
            room_id (str): The room ID to insert the question into.
            question_id (str): The question object id.
            option_id (str): The option object id.

        Returns:
            bool: True if the question is successfully inserted, False otherwise.
        """
        list_of_questions = self.get_questions(room_id=room_id)
        for question in list_of_questions:
            if question["question_id"] == question_id:
                for option in question["options"]:
                    if option["option_id"] == option_id:
                        option["votes"] -= 1

        if self.store_single_field(
            room_id=room_id, field="questions", data=list_of_questions, replace=True
        ):
            return True
        else:
            return False

    def update_room_activity_time(self, room_id: str, data: datetime) -> bool:
        """
        Update the last activity timestamp for a room in the database.

        Args:
            room_id (str): The room ID to update.
            data (datetime): A datetime object representing the new activity time.
        """
        return self.store_single_field(
            room_id=room_id, field="last_activity", data=data, replace=True
        )

    def get_room_location(self, room_id: str) -> str:
        """
        Get the location of a room from the database.

        Args:
            room_id (str): The room ID to retrieve the location for.

        Returns:
            str: The room's location.
        """
        return self._query_single_field(room_id=room_id, field="room_location")

    def update_room_location(self, room_id: str, data: str) -> bool:
        """
        Update the location of a room in the database.

        Args:
            room_id (str): The room ID to update.
            data (str): The new location data.

        Returns:
            bool: True if the location is successfully updated, False otherwise.
        """
        return self.store_single_field(
            room_id=room_id, field="room_location", data=data, replace=True
        )

    def get_room_activity(self, room_id: str) -> str:
        """
        Get the activity of a room from the database.

        Args:
            room_id (str): The room ID to retrieve the activity for.

        Returns:
            str: The room's activity.
        """
        return self._query_single_field(room_id=room_id, field="room_location")

    def update_room_activity(self, room_id: str, data: str) -> bool:
        """
        Update the activity of a room in the database.

        Args:
            room_id (str): The room ID to update.
            data (str): The new activity data.

        Returns:
            bool: True if the activity is successfully updated, False otherwise.
        """
        return self.store_single_field(
            room_id=room_id, field="room_activity", data=data, replace=True
        )

    def query_all_hash_keys(self):
        """
        Query all hash keys in the Redis database and print field-value pairs.
        """
        hash_keys = [i.decode("utf-8") for i in self.r.keys("*")]
        # print("hash_keys:", hash_keys)
        # for key in hash_keys:
        # field_value_pairs = self.r.hgetall(key)
        # print(f"Hash Key: {key}")
        # print("Field-Value Pairs:")
        # print(f"{field_value_pairs}")
        return hash_keys


if __name__ == "__main__":
    pass
