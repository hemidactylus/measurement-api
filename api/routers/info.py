"""
    info.py
"""


from fastapi import APIRouter, Depends
from loguru import logger

from api.database.dbAccess import (getDbSession, countHitsForCaller,
                                   checkTotalHits, getRateInfo)
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

    rateInfo = await getRateInfo(caller, cassandra)

    if settings.debug:
        logger.info('caller = %s' % caller)
        logger.info('rateTotal = %s' % rateInfo['total'])
        logger.info('rateConsumed = %s' % rateInfo['consumed'])

    return rateInfo
