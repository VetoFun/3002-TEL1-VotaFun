import redis
import json
from typing import List, Dict, Union

from src.logger import logger
from .Option import Option
from .Question import Question
from .Room import Room
from .User import User


class Database:
    def __init__(
        self, redis_url: str = "", redis_host: str = "localhost", redis_port: int = 6379
    ) -> None:
        if not redis_url:
            redis_url = f"redis://@{redis_host}:{redis_port}"
        self.r = redis.from_url(redis_url)

    def query_room_data(self, room_id: str, return_dict=False) -> Union[Room, Dict]:
        if not self.r.exists(room_id):
            raise KeyError(f"Error: {room_id} does not exist.")
        room_data_byte = self.r.hgetall(room_id)
        room_data = {}
        for key, value in room_data_byte.items():
            room_data[key.decode("utf-8")] = value.decode("utf-8")
        room = Room.from_dict(room_data)
        if return_dict:
            return room.to_dict()
        return room

    def store_room_data(self, room_id: str, room_data: Room) -> None:
        # Store room data in Redis Hash
        for key, value in room_data.to_dict().items():
            self.r.hset(room_id, key, json.dumps(value))
        logger.info(f"Room {room_id} successfully stored.")

    def remove_room_data(self, room_id: str) -> int:
        # returns number of rooms deleted
        return self.r.delete(room_id)

    def get_users(self, room_id: str) -> List[Dict[str, str]]:
        room = self.query_room_data(room_id=room_id)
        return [user.to_dict() for user in room.users]

    def add_user(self, room_id: str, user_id: str, username: str) -> int:
        room = self.query_room_data(room_id=room_id)
        new_user = User(user_id=user_id, user_name=username)
        room.add_user(new_user)
        self.store_room_data(room_id=room_id, room_data=room)
        return len(room.users)

    def remove_user(self, room_id: str, user_id: str) -> int:
        room = self.query_room_data(room_id=room_id)
        room.remove_user_from_id(user_id=user_id)
        self.store_room_data(room_id=room_id, room_data=room)
        return len(room.users)

    def get_questions(
        self, room_id: str
    ) -> List[Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]]:
        room = self.query_room_data(room_id=room_id)
        return [question.to_dict() for question in room.questions]

    def add_question(self, room_id: str, question_id: str, question_text: str) -> int:
        question = Question(question_id=question_id, question_text=question_text)
        room = self.query_room_data(room_id=room_id)
        room.add_question(question=question)
        self.store_room_data(room_id=room_id, room_data=room)
        return len(room.questions)

    def get_options(self, room_id: str, question_id: str) -> List[Dict]:
        room = self.query_room_data(room_id=room_id)
        question = room.get_question_from_id(question_id=question_id)
        return [option.to_dict() for option in question.options]

    def add_option(
        self, room_id: str, question_id: str, option_id: str, option_text: str
    ) -> int:
        option = Option(option_id=option_id, option_text=option_text)
        room = self.query_room_data(room_id=room_id)
        question = room.get_question_from_id(question_id=question_id)
        question.add_option(option=option)
        self.store_room_data(room_id=room_id, room_data=room)
        return len(question.options)

    def get_vote(self, room_id: str, question_id: str, option_id: str) -> int:
        room = self.query_room_data(room_id=room_id)
        question = room.get_question_from_id(question_id=question_id)
        option = question.get_option_by_id(option_id=option_id)
        return option.current_votes

    def increment_vote(
        self, room_id: str, question_id: str, option_id: str, num_votes: int = 1
    ) -> int:
        room = self.query_room_data(room_id=room_id)
        question = room.get_question_from_id(question_id=question_id)
        option = question.get_option_by_id(option_id=option_id)
        option.add_vote(num_votes=num_votes)
        self.store_room_data(room_id=room_id, room_data=room)
        return option.current_votes

    def set_vote(
        self, room_id: str, question_id: str, option_id: str, num_votes: int
    ) -> int:
        room = self.query_room_data(room_id=room_id)
        question = room.get_question_from_id(question_id=question_id)
        option = question.get_option_by_id(option_id=option_id)
        option.set_vote(num_votes=num_votes)
        self.store_room_data(room_id=room_id, room_data=room)
        return option.current_votes

    def update_room_activity_time(self, room_id: str, activity_time: str) -> str:
        room = self.query_room_data(room_id=room_id)
        room.last_activity = activity_time
        self.store_room_data(room_id=room_id, room_data=room)
        return activity_time
