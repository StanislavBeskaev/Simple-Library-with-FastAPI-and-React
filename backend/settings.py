from pydantic import BaseSettings


class Settings(BaseSettings):
    pg_host: str = 'localhost'
    init_data_type: str = 'test_1000_1000000'


settings = Settings()
