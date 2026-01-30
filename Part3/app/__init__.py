class Config:
    """Base configuration class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = "super-secret-key"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
