"""
    callerID.py
"""

from fastapi import Header, Request, HTTPException
from typing import Optional
import hashlib

from api.helpers.Caller import Caller
from api.settings import getSettings


def getCaller(*, X_API_Key: Optional[str] = Header(None), req: Request,
              X_Customer_ID: Optional[str] = Header(None)):
    """
        Identify the caller (whether anonymous or key-bearer).
        Return a Caller object.
    """
    if X_Customer_ID is None:
        prefixed = '%s%s' % (
            getSettings().hashPrefix,
            req.client.host,
        )
        return Caller(
            anonymous=True,
            callerID=hashlib.md5(prefixed.encode()).hexdigest(),
        )
    else:
        if X_API_Key is None:
            raise HTTPException(401, 'Missing "X-API-Key" header.')
        else:
            return Caller(
                anonymous=False,
                callerID=X_Customer_ID,
                APIKey=X_API_Key,
            )
