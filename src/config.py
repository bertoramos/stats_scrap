
from pydantic import HttpUrl
from pydantic_settings import BaseSettings # NEW
from functools import lru_cache
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".config")

class Settings(BaseSettings):
    source_url: HttpUrl = "http://empty.none"
    retry_attempts: int = -1
    timeout_seconds: int = -1

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"

# Cargamos solo una vez, como un singleton
@lru_cache
def get_settings():
    return Settings()
