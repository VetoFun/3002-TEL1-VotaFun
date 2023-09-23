import os
import pytest
import redis


# Mock Redis connection for testing
@pytest.fixture
def mock_redis():
    redis_url = os.environ.get("REDIS_URL", "redis://@localhost:6379/0")
    return redis.StrictRedis.from_url(redis_url)
