"""
    info.py
"""


from fastapi import APIRouter, Depends

from api.database.dbAccess import (getDbSession, countHitsForCaller,
                                   checkTotalHits)
from api.helpers.callerID import getCallerIDPair
from api.settings import getSettings


infoRouter = APIRouter()

@infoRouter.get('/rate_available')
async def rate_available(cassandra=Depends(getDbSession),
                         callerIDPair=Depends(getCallerIDPair)):
    """
    Return info on current rate count for the caller.
    """
    settings = getSettings()
    callerID, callerAPIKey = callerIDPair

    if settings.debug:
        print('[rate_available] callerID = %s' % callerID)
        print('[rate_available] callerApiKey = %s' % callerAPIKey)

    # get client rate available
    rateTotal = await checkTotalHits(callerID, callerAPIKey, cassandra)
    if settings.debug:
        print('[rate_available] rateTotal = %s' % rateTotal)

    # count request in last timespan
    rateConsumed = await countHitsForCaller(callerID, cassandra)
    if settings.debug:
        print('[rate_available] rateConsumed = %s' % rateConsumed)

    return {
        'window_seconds': settings.rateLimitWindowSeconds,
        'consumed': rateConsumed,
        'total': rateTotal,
        'available': rateTotal - rateConsumed,
    }
