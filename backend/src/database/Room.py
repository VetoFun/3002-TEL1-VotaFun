from typing import List, Dict, Union, Optional
from src.database.Question import Question
from src.database.User import User
import json


class Room:
    """
    Represents a Room with various attributes.

    Args:
        room_id (str): The unique identifier for the room.
        room_code (str): The room code or name.
        number_of_user (int): The number of users in the room.
        max_capacity (int): The maximum capacity of the room.
        last_activity (str): The timestamp of the room's last activity.
        questions (list, optional): List of Question objects. Defaults to an
        empty list.
        host_id (str, optional): The user ID of the room host. Defaults to an
        empty string.
        status (str, optional): The status of the room. Defaults to an empty
        string.
        room_location (str, optional): The location of the room. Defaults to
        an empty string.
        room_activity (str, optional): The activity description of the room.
        Defaults to an empty string.
        users (list, optional): List of User objects. Defaults to an empty
        list.
    """

    def __init__(
        self,
        room_id: str,
        room_code: str,
        number_of_user: int,
        max_capacity: int,
        last_activity: str,
        questions: Optional[List[Question]] = None,
        host_id: str = "",
        status: str = "",
        room_location: str = "",
        room_activity: str = "",
        users: Optional[List[User]] = None,
    ):
        self.room_id = room_id
        self.room_code = room_code
        self.number_of_user = number_of_user
        self.max_capacity = max_capacity
        self.last_activity = last_activity
        self.questions = questions or []
        self.host_id = host_id
        self.status = status
        self.room_location = room_location
        self.room_activity = room_activity
        self.users = users or []

    def __eq__(self, other):
        if not isinstance(other, Room):
            return False
        return (
            self.room_id == other.room_id
            and self.room_code == other.room_code
            and self.number_of_user == other.number_of_user
            and self.max_capacity == other.max_capacity
            and self.last_activity == other.last_activity
            and self.questions == other.questions
            and self.host_id == other.host_id
            and self.status == other.status
            and self.room_location == other.room_location
            and self.room_activity == other.room_activity
            and self.users == other.users
        )

    def add_user(self, user: User):
        self.users.append(user)

    def add_question(self, question: Question):
        self.questions.append(question)

    def to_dict(self) -> Dict[str, Union[str, int, List[Dict[str, Union[str, int]]]]]:
        return {
            "room_id": self.room_id,
            "room_code": self.room_code,
            "number_of_user": self.number_of_user,
            "max_capacity": self.max_capacity,
            "last_activity": self.last_activity,
            "questions": [question.to_dict() for question in self.questions],
            "host_id": self.host_id,
            "status": self.status,
            "room_location": self.room_location,
            "room_activity": self.room_activity,
            "users": [user.to_dict() for user in self.users],
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a Room object from a dictionary.

        Args:
            data (dict): A dictionary containing room data.

        Returns:
            Room: A Room object.
        """
        # Extract values from the dictionary
        room_id = eval(data.get("room_id", ""))
        room_code = eval(data.get("room_code", ""))
        number_of_user = eval(data.get("number_of_user", 0))
        max_capacity = eval(data.get("max_capacity", 0))
        last_activity = eval(data.get("last_activity", ""))
        host_id = eval(data.get("host_id", ""))
        status = eval(data.get("status", ""))
        room_location = eval(data.get("room_location", ""))
        room_activity = eval(data.get("room_activity", ""))
        questions = [
            Question.from_dict(q) for q in json.loads(data.get("questions", []))
        ]
        users = [User.from_dict(u) for u in json.loads(data.get("users", []))]

        # Create and return a Room object
        return cls(
            room_id=room_id,
            room_code=room_code,
            number_of_user=number_of_user,
            max_capacity=max_capacity,
            last_activity=last_activity,
            host_id=host_id,
            status=status,
            room_location=room_location,
            room_activity=room_activity,
            questions=questions,
            users=users,
        )
