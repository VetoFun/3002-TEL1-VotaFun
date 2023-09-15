import os


class Config:
    REDIS_URL = os.environ.get("REDIS_URL", "")
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))


class DevelopmentConfig(Config):
    # Development-specific configuration settings go here
    DEBUG = True


class TestingConfig(Config):
    # Testing-specific configuration settings go here
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    # Production-specific configuration settings go here
    DEBUG = False
