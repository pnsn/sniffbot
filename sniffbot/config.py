import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SNIFFBOT_SECRET')
    EWORM_USER = os.getenv('EWORM_USER')
    EWORM_HOST_STAGING = os.getenv('EWORM_HOST_STAGING')
    EWORM_HOST_PRODUCTION = os.getenv('EWORM_HOST_PRODUCTION')
    EWORM_RING = os.getenv('EWORM_RING')
    SSH_I_FILE = os.getenv('SSH_I_FILE')


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
