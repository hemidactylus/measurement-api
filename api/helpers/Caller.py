"""
    Caller.py
"""

from pydantic import BaseModel
from typing import Optional


class Caller(BaseModel):
    anonymous: bool
    callerID: str
    APIKey: Optional[str] = None
