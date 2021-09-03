"""
    info.py
"""


from fastapi import APIRouter, Depends
from loguru import logger

from api.database.dbAccess import (getDbSession, countHitsForCaller,
                                   checkTotalHits)
from api.helpers.callerID import getCaller
from api.settings import getSettings


infoRouter = APIRouter()


@infoRouter.get('/rate_available')
async def rate_available(cassandra=Depends(getDbSession),
                         caller=Depends(getCaller)):
    """
    Return info on current rate count for the caller.
    """
    settings = getSettings()

    if settings.debug:
        logger.info('[rate_available] caller = %s' % caller)

    # get client rate available
    rateTotal = await checkTotalHits(caller, cassandra)
    if settings.debug:
        logger.info('[rate_available] rateTotal = %s' % rateTotal)

    # count request in last timespan
    rateConsumed = await countHitsForCaller(caller, cassandra)
    if settings.debug:
        logger.info('[rate_available] rateConsumed = %s' % rateConsumed)

    return {
        'window_seconds': settings.rateLimitWindowSeconds,
        'consumed': rateConsumed,
        'total': rateTotal,
        'available': rateTotal - rateConsumed,
    }
