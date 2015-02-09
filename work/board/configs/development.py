from board.configs.default import DefaultConfig


class DevelopmentConfig(DefaultConfig):

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProfileConfig(DefaultConfig):
    DEBUG = True
    PROFILE = True
    SQLALCHEMY_ECHO = True
