import redis
import json
from typing import List, Dict, Union

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
            redis_url = f"redis://{redis_host}:{redis_port}"
        self.r = redis.from_url(redis_url)

    def query_room_data(
        self, room_id: str, pipeline: redis.Redis.pipeline = None, return_dict=False
    ) -> Union[Room, Dict]:
        if not pipeline:
            raise ValueError("Redis pipeline has to be provided")
        if not pipeline.exists(room_id):
            raise KeyError(f"Error: room {room_id} does not exist.")
        room_data_byte = pipeline.hgetall(room_id)
        room_data = {}
        for key, value in room_data_byte.items():
            room_data[key.decode("utf-8")] = value.decode("utf-8")
        room = Room.from_dict(room_data)
        if return_dict:
            return room.to_dict()
        return room

    def store_room_data(
        self, room_id: str, room_data: Room, pipeline: redis.Redis.pipeline = None
    ) -> None:
        if not pipeline:
            raise ValueError("Redis pipeline has to be provided")
        # Store room data in Redis Hash
        for key, value in room_data.to_dict().items():
            pipeline.hset(room_id, key, json.dumps(value))
        logger.info(f"Room {room_id} successfully stored.")

    @redis_pipeline
    def remove_room_data(
        self, room_id: str, pipeline: redis.Redis.pipeline = None
    ) -> int:
        # returns number of rooms deleted
        return pipeline.delete(room_id)

    @redis_pipeline
    def get_users(
        self, room_id: str, pipeline: redis.Redis.pipeline = None
    ) -> List[Dict[str, str]]:
        room = self.query_room_data(room_id=room_id, pipeline=pipeline)
        return [user.to_dict() for user in room.users]

    @redis_pipeline
    def add_user(
        self,
        room_id: str,
        user_id: str,
        username: str,
        pipeline: redis.Redis.pipeline = None,
    ) -> int:
        room = self.query_room_data(room_id=room_id, pipeline=pipeline)
        new_user = User(user_id=user_id, user_name=username)
        room.add_user(new_user)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return len(room.users)

    @redis_pipeline
    def remove_user(
        self, room_id: str, user_id: str, pipeline: redis.Redis.pipeline = None
    ) -> None:
        room = self.query_room_data(room_id=room_id, pipeline=pipeline)
        room.remove_user_from_id(user_id=user_id)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return len(room.users)

    @redis_pipeline
    def get_questions(
        self, room_id: str, pipeline: redis.Redis.pipeline = None
    ) -> List[Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]]:
        room = self.query_room_data(room_id=room_id, pipeline=pipeline)
        return [question.to_dict() for question in room.questions]

    @redis_pipeline
    def add_question(
        self,
        room_id: str,
        question_id: str,
        question_text: str,
        pipeline: redis.Redis.pipeline = None,
    ) -> int:
        question = Question(question_id=question_id, question_text=question_text)
        room = self.query_room_data(room_id=room_id, pipeline=pipeline)
        room.add_question(question=question)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return len(room.questions)

    @redis_pipeline
    def get_options(
        self, room_id: str, question_id: str, pipeline: redis.Redis.pipeline = None
    ) -> List[Dict]:
        room = self.query_room_data(room_id=room_id, pipeline=pipeline)
        question = room.get_question_from_id(question_id=question_id)
        return [option.to_dict() for option in question.options]

    @redis_pipeline
    def add_option(
        self,
        room_id: str,
        question_id: str,
        option_id: str,
        option_text: str,
        pipeline: redis.Redis.pipeline = None,
    ) -> int:
        option = Option(option_id=option_id, option_text=option_text)
        room = self.query_room_data(room_id=room_id, pipeline=pipeline)
        question = room.get_question_from_id(question_id=question_id)
        question.add_option(option=option)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return len(question.options)

    @redis_pipeline
    def get_vote(
        self,
        room_id: str,
        question_id: str,
        option_id: str,
        pipeline: redis.Redis.pipeline = None,
    ) -> int:
        room = self.query_room_data(room_id=room_id, pipeline=pipeline)
        question = room.get_question_from_id(question_id=question_id)
        option = question.get_option_by_id(option_id=option_id)
        return option.current_votes

    @redis_pipeline
    def increment_vote(
        self,
        room_id: str,
        question_id: str,
        option_id: str,
        num_votes: int = 1,
        pipeline: redis.Redis.pipeline = None,
    ) -> int:
        room = self.query_room_data(room_id=room_id, pipeline=pipeline)
        question = room.get_question_from_id(question_id=question_id)
        option = question.get_option_by_id(option_id=option_id)
        option.add_vote(num_votes=num_votes)
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return option.current_votes

    @redis_pipeline
    def update_room_activity_time(
        self, room_id: str, activity_time: str, pipeline: redis.Redis.pipeline = None
    ) -> str:
        room = self.query_room_data(room_id=room_id, pipeline=pipeline)
        room.last_activity = activity_time
        self.store_room_data(room_id=room_id, room_data=room, pipeline=pipeline)
        return activity_time
