import os
from functools import lru_cache


class BaseConfig:
    SECRET_KEY = "shevdetdcetcdegthemInfTheMarketjebfhebf"
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    DATABASE_URL: str = "sqlite:///./hacker.db"

    MAIL_CONFIG = {
        "EMAIL_PASSWORD": EMAIL_PASSWORD,
        "EMAIL_PORT": EMAIL_PORT,
        "EMAIL_HOST": EMAIL_HOST,
        "EMAIL_USERNAME": EMAIL_USERNAME,
    }


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    DATABASE_URL: str = "sqlite:///./test.db"
    DATABASE_CONNECT_DICT: dict = {"check_same_thread": False}


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_name = os.environ.get("PIPELINE_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
