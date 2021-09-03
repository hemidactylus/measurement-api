"""
    measurement.py
"""


from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.database.dbAccess import (getDbSession, countHitsForCaller,
                                   checkTotalHits, logRequest)
from api.helpers.callerID import getCaller
from api.settings import getSettings

from dimLib.analyzer import validate, getAllUnitSymbols, getUnitInfo
from dimLib.formatting import dress


class ValidationRequest(BaseModel):
    text: str


measurementRouter = APIRouter()


@measurementRouter.post('/validate')
async def validate_measurement(v_request: ValidationRequest,
                               cassandra=Depends(getDbSession),
                               caller=Depends(getCaller)):
    """
    Validate a measurement.
    """
    settings = getSettings()

    if settings.debug:
        print('[validate_measurement] caller = %s' % caller)

    # get client rate available
    rateTotal = await checkTotalHits(caller, cassandra)
    if settings.debug:
        print('[validate_measurement] rateTotal = %s' % rateTotal)

    # count request in last timespan
    rateConsumed = await countHitsForCaller(caller, cassandra)
    if settings.debug:
        print('[validate_measurement] rateConsumed = %s' % rateConsumed)

    if rateTotal <= rateConsumed:
        raise HTTPException(429)
    else:
        # schedule marking this request for this client
        await logRequest(caller, v_request.text, cassandra)

        # return
        return dress(validate(v_request.text))


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
