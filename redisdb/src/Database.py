import redis

class Database:
    def __init__(self):
        self.connection = redis.Redis(host='localhost', port=6379)

    def query(self):
        pass

    def store(self):
        pass