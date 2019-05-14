import os
BASE_DIR = os.path.abspath(os.path.dirname(__name__))


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
    TESTING = True
    WTF_CSRF_ENABLED = False
