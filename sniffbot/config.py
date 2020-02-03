import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SNIFFBOT_SECRET')
    EWORM_USER = os.getenv('EWORM_USER')
    EWORM_HOST = os.getenv('EWORM_HOST')
    EWORM_RING = os.getenv('EWORM_RING')


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
