import redis
import json
from typing import List, Dict, Union, Tuple
from datetime import datetime
from hashlib import sha1

from ..logger import logger
from ..decorators import redis_pipeline
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
            raise KeyError(f"Error: room {room_id} does not exist.")
        room_data_byte = self.r.hgetall(room_id)
        room_data = {}
        for key, value in room_data_byte.items():
            room_data[key.decode("utf-8")] = value.decode("utf-8")
        room = Room.from_dict(room_data)
        if return_dict:
            return room.to_dict()
        return room

    def store_room_data(
        self, room_id: str, room_data: Room, pipeline: redis.Redis.pipeline
    ) -> None:
        # Store room data in Redis Hash
        for key, value in room_data.to_dict().items():
            pipeline.hset(room_id, key, json.dumps(value))
        pipeline.execute()
        logger.info(f"Room {room_id} successfully stored.")

    @redis_pipeline
    def remove_room_data(self, room_id: str, pipeline: redis.Redis.pipeline) -> int:
        # returns number of rooms deleted
        pipeline.delete(room_id)
        return pipeline.execute()[0]

    def get_users(self, room_id: str) -> List[Dict[str, str]]:
        room = self.query_room_data(room_id=room_id)
        return [user.to_dict() for user in room.users]

    @redis_pipeline
    def add_user(
        self,
        room_id: str,
        user_id: str,
        username: str,
        pipeline: redis.Redis.pipeline,
    ) -> int:
        room = self.query_room_data(room_id=room_id)
        if room.get_number_of_user() == room.get_max_capacity():
            raise Exception(f"Room {room_id} is at max capacity")
        new_user = User(user_id=user_id, user_name=username)
        room.add_user(new_user)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return len(room.users)

    @redis_pipeline
    def remove_user(
        self, room_id: str, user_id: str, pipeline: redis.Redis.pipeline
    ) -> Tuple[int, bool]:
        room = self.query_room_data(room_id=room_id)
        is_host = False
        try:
            room.remove_user_from_id(user_id=user_id)
            is_host = user_id == room.host_id
        except KeyError as e:
            logger.error(e)
            return len(room.users), False
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return len(room.users), is_host

    def get_questions(
        self, room_id: str
    ) -> List[Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]]:
        room = self.query_room_data(room_id=room_id)
        return [question.to_dict() for question in room.questions]

    @redis_pipeline
    def add_question_and_options(
        self,
        room_id: str,
        question_id: str,
        question_text: str,
        options: List[Tuple[str, str]],
        pipeline: redis.Redis.pipeline,
    ) -> int:
        question = Question(question_id=question_id, question_text=question_text)
        for option_id, option_text in options:
            question.add_option(Option(option_id=option_id, option_text=option_text))
        room = self.query_room_data(room_id=room_id)
        room.add_question(question=question)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return len(room.questions)

    def get_options(self, room_id: str, question_id: str) -> List[Dict]:
        room = self.query_room_data(room_id=room_id)
        question = room.get_question_from_id(question_id=question_id)
        return [option.to_dict() for option in question.options]

    @redis_pipeline
    def add_option(
        self,
        room_id: str,
        question_id: str,
        option_id: str,
        option_text: str,
        pipeline: redis.Redis.pipeline,
    ) -> int:
        option = Option(option_id=option_id, option_text=option_text)
        room = self.query_room_data(room_id=room_id)
        question = room.get_question_from_id(question_id=question_id)
        question.add_option(option=option)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return len(question.options)

    def get_vote(
        self,
        room_id: str,
        question_id: str,
        option_id: str,
    ) -> int:
        room = self.query_room_data(room_id=room_id)
        question = room.get_question_from_id(question_id=question_id)
        option = question.get_option_by_id(option_id=option_id)
        return option.current_votes

    @redis_pipeline
    def increment_vote(
        self,
        room_id: str,
        question_id: str,
        option_id: str,
        pipeline: redis.Redis.pipeline,
        num_votes: int = 1,
    ) -> int:
        room = self.query_room_data(room_id=room_id)
        question = room.get_question_from_id(question_id=question_id)
        option = question.get_option_by_id(option_id=option_id)
        option.add_vote(num_votes=num_votes)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return option.current_votes

    @redis_pipeline
    def set_vote(
        self,
        room_id: str,
        question_id: str,
        option_id: str,
        num_votes: int,
        pipeline: redis.Redis.pipeline,
    ) -> int:
        room = self.query_room_data(room_id=room_id)
        question = room.get_question_from_id(question_id=question_id)
        option = question.get_option_by_id(option_id=option_id)
        option.set_vote(num_votes=num_votes)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return option.current_votes

    @redis_pipeline
    def update_room_activity_time(
        self, room_id: str, activity_time: str, pipeline: redis.Redis.pipeline
    ) -> str:
        room = self.query_room_data(room_id=room_id)
        room.last_activity = activity_time
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return activity_time

    def query_room_id_from_user_id(self, user_id: str) -> str:
        for room_id in self.r.scan_iter():
            room = self.query_room_data(room_id=room_id)
            for user in room.users:
                if user.user_id == user_id:
                    return room_id
        raise KeyError(f"User {user_id} does not exist in any room")

    @redis_pipeline
    def create_room(self, pipeline: redis.Redis.pipeline) -> Room:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        room_id = sha1(timestamp.encode("utf-8")).hexdigest()
        if self.r.exists(room_id):
            raise ValueError(f"Room {room_id} already exists.")
        room = Room(room_id=room_id)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return room_id

    @redis_pipeline
    def change_host(
        self, room_id: str, new_host_id: str, pipeline: redis.Redis.pipeline
    ) -> None:
        room = self.query_room_data(room_id=room_id)
        room.set_host(new_host_id=new_host_id)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return
