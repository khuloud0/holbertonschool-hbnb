class Config:
    """Base configuration class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = "super-secret-key"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///hbnb_dev.db"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///hbnb_test.db"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///hbnb_prod.db"
