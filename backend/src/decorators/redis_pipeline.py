import redis
from functools import wraps


def redis_pipeline(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        room_id = kwargs.get("room_id")
        with self.r.pipeline() as pipe:
            for _ in range(5):
                try:
                    pipe.watch(room_id)
                    pipe.multi()
                    return func(self, pipeline=pipe, *args, **kwargs)
                except redis.exceptions.WatchError:
                    continue
        raise Exception("Watch operation failed 5 times consecutively.")

    return wrapper