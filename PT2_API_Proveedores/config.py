from os import environ

class Config(object):
    """Base configuration."""

    #DB_HOST = "bd_name"
    #DB_USER = "db_user"
    #DB_PASS = "db_pass"
    #DB_NAME = "db_name"
    pass

class ProductionConfig(Config):
    """Production configuration."""

    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "grupo24")
    DB_PASS = environ.get("DB_PASS", "M2MzZjBlMzZlOWRj")
    DB_NAME = environ.get("DB_NAME", "grupo24")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


class DevelopmentConfig(Config):
    """Development configuration."""

    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "root")
    DB_PASS = environ.get("DB_PASS", "root")
    DB_NAME = environ.get("DB_NAME", "grupo5_supplier")
    #DB_PORT = environ.get("DB_PORT", "5000")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/grupo5_supplier"
    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}