import yaml
from pydantic import BaseModel, HttpUrl
from typing import Literal, List
from functools import lru_cache
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

# Modelo para cada URL
class URLItem(BaseModel):
    type: Literal["ISTAC_SURVEY"]
    url: HttpUrl

# Modelo principal
class Settings(BaseModel):
    debug: bool
    retry_attempts: int
    timeout_seconds: int
    urls: List[URLItem]

@lru_cache
def get_settings():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Settings(**data)
