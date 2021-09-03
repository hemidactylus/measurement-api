"""
    settings.py
"""

from functools import lru_cache
from pydantic import BaseSettings
import json

from configuration.config import defaultRateLimitWindowSeconds, defaultAnonymousRateAllowed, secrets_json_path
secrets = json.load(open(secrets_json_path))


class Settings(BaseSettings):
    clientID: str = secrets['clientID']
    clientSecret: str = secrets['clientSecret']
    hashPrefix: str = secrets['hashPrefix']
    debug: bool = False
    rateLimitWindowSeconds: int = defaultRateLimitWindowSeconds
    anonymousRateAllowed: int = defaultAnonymousRateAllowed

@lru_cache()
def getSettings():
    return Settings()
