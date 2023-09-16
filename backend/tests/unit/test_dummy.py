def test_dummy_with_fake_redis(fake_redis):
    # Perform some operations using fake_redis
    fake_redis.set("key1", "value1")
    fake_redis.hset("hash_key", "field1", "field_value1")

    # Retrieve data and assert
    assert fake_redis.get("key1") == b"value1"
    assert fake_redis.hget("hash_key", "field1") == b"field_value1"
