"""
    callerID.py
"""

from fastapi import Header, Request, HTTPException
from typing import Optional
import hashlib

from api.settings import getSettings


def getCallerIDPair(*, X_API_Key: Optional[str] = Header(None), req: Request,
                    X_Customer_ID: Optional[str] = Header(None)) -> str:
    """
        Identify the caller (whether anonymous or key-bearer).
        Return (callerID, API Key or None).
    """
    if X_Customer_ID is None:
        prefixed = '%s%s' % (
            getSettings().hashPrefix,
            req.client.host,
        )
        return ('a_%s' % hashlib.md5(prefixed.encode()).hexdigest(), None)
    else:
        if X_API_Key is None:
            raise HTTPException(401, 'Please provide an API Key through the "X-Customer-ID" header.')
        else:
            return ('c_%s' % X_Customer_ID, X_API_Key)
