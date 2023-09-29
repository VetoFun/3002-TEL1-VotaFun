import json
from typing import List, Dict, Union
from enum import Enum, auto
from datetime import datetime, timedelta

from .Question import Question
from .User import User
from ..config import Config


class RoomStatus(str, Enum):
    WAITING = auto()
    STARTED = auto()


class Room:
    """
    Represents a Room with various attributes.

    Args:
        room_id (str): The unique identifier for the room.
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
        number_of_user: int = 0,
        max_capacity: int = Config.MAX_CAPACITY,
        last_activity: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        questions: List[Question] = [],
        host_id: str = "",
        status: str = RoomStatus.WAITING,
        room_location: str = "",
        room_activity: str = "",
        users: List[User] = [],
    ):
        self.room_id = room_id
        self.number_of_user = number_of_user
        self.max_capacity = max_capacity
        self.last_activity = last_activity
        self.questions = questions
        self.host_id = host_id
        self.status = status
        self.room_location = room_location
        self.room_activity = room_activity
        self.users = users

    def __eq__(self, other):
        if not isinstance(other, Room):
            return False
        return (
            self.room_id == other.room_id
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

    def get_question_from_id(self, question_id: str) -> Question:
        for question in self.questions:
            if question.question_id == question_id:
                return question
        raise KeyError(f"Question {question_id} does not exist in room {self.room_id}")

    def get_user_from_id(self, user_id: str) -> User:
        for user in self.users:
            if user.user_id == user_id:
                return user
        raise KeyError(f"User {user_id} does not exist in room {self.room_id}")

    def add_user(self, user: User):
        self.users.append(user)
        self.number_of_user += 1

    def remove_user_from_id(self, user_id: str) -> int:
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)
                self.number_of_user -= 1
                return len(self.users)
        raise KeyError(f"User {user_id} does not exist in room {self.room_id}")

    def add_question(self, question: Question):
        self.questions.append(question)

    def get_number_of_user(self):
        return self.number_of_user

    def get_max_capacity(self):
        return self.max_capacity

    def set_host(self, new_host_id):
        self.host_id = new_host_id

    def set_activity(self, room_activity):
        self.room_activity = room_activity

    def set_location(self, room_location):
        self.room_location = room_location

    def start_room(self):
        self.status = RoomStatus.STARTED

    def is_room_still_active(self, time: datetime) -> bool:
        last_activity = datetime.strptime(self.last_activity, "%Y-%m-%d %H:%M:%S")
        return time - last_activity <= timedelta(hours=1)

    def to_dict(self) -> Dict[str, Union[str, int, List[Dict[str, Union[str, int]]]]]:
        return {
            "room_id": self.room_id,
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
        room_id = data.get("room_id").strip('"')
        number_of_user = int(data.get("number_of_user", 0))
        max_capacity = int(data.get("max_capacity", Config.MAX_CAPACITY))
        last_activity = data.get("last_activity", "").strip('"')
        host_id = data.get("host_id", "").strip('"')
        status = eval(data.get("status", RoomStatus.WAITING))
        room_location = data.get("room_location", "").strip('"')
        room_activity = data.get("room_activity", "").strip('"')
        questions = (
            [Question.from_dict(q) for q in json.loads(data.get("questions"))]
            if "questions" in data
            else []
        )
        users = (
            [User.from_dict(u) for u in json.loads(data.get("users", ""))]
            if "users" in data
            else []
        )

        # Create and return a Room object
        return cls(
            room_id=room_id,
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
