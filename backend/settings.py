from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_connection_url: str = "postgresql://postgres:postgres@localhost:5432/postgres"
    init_data_type: str = 'test_1000_1000000'


def get_settings() -> Settings:
    return Settings()

