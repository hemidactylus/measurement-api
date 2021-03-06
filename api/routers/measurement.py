"""
    measurement.py
"""


from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from loguru import logger

from api.database.dbAccess import (getDbSession, countHitsForCaller,
                                   checkTotalHits, logRequest, getRateInfo)
from api.helpers.callerID import getCaller
from api.settings import getSettings

from dimLib.analyzer import validate, getAllUnitSymbols, getUnitInfo
from dimLib.formatting import dress


class ValidationRequest(BaseModel):
    text: str


measurementRouter = APIRouter()


@measurementRouter.post('/validate')
async def validate_measurement(v_request: ValidationRequest,
                               bg_tasks: BackgroundTasks,
                               cassandra=Depends(getDbSession),
                               caller=Depends(getCaller)):
    """
    Validate a measurement.
    """
    settings = getSettings()

    rateInfo = await getRateInfo(caller, cassandra)

    if settings.debug:
        logger.info('caller = %s' % caller)
        logger.info('rateTotal = %s' % rateInfo['total'])
        logger.info('rateConsumed = %s' % rateInfo['consumed'])

    if rateInfo['total'] <= rateInfo['consumed']:
        raise HTTPException(429)
    else:
        # schedule logging this request to run as a deferred call ...
        bg_tasks.add_task(
            logRequest,
            caller,
            v_request.text,
            cassandra,
        )
        # ... validate the input expression (and 'dress' it) ...
        dressedResult = dress(validate(v_request.text))
        # and finally return it to the caller:
        return dressedResult


@measurementRouter.get('/units')
async def get_all_units():
    """
    Get a list of all known unit symbols.
    """
    return sorted(getAllUnitSymbols())


@measurementRouter.get('/unit/{unitSymbol}')
async def get_unit_info(unitSymbol: str):
    """
    Get some info on a particular unit.
    """
    unitInfo = getUnitInfo(unitSymbol)
    if unitInfo is not None:
        return unitInfo
    else:
        return HTTPException(404, 'Unknown symbol.')
