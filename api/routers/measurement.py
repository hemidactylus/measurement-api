"""
    measurement.py
"""


from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.database.dbAccess import (getDbSession, countHitsForCaller,
                                   checkTotalHits, logRequest)
from api.helpers.callerID import getCallerIDPair
from api.settings import getSettings

from dimLib.analyzer import validate, getAllUnitSymbols
from dimLib.formatting import dress


class ValidationRequest(BaseModel):
    text: str


measurementRouter = APIRouter()


@measurementRouter.post('/validate')
async def validate_measurement(v_request: ValidationRequest,
                               cassandra=Depends(getDbSession),
                               callerIDPair=Depends(getCallerIDPair)):
    """
    Validate a measurement.
    """
    settings = getSettings()
    callerID, callerAPIKey = callerIDPair

    # get client ID
    if settings.debug:
        print('[validate_measurement] callerID = %s' % callerID)
        print('[validate_measurement] callerApiKey = %s' % callerAPIKey)

    # get client rate available
    rateTotal = await checkTotalHits(callerID, callerAPIKey, cassandra)
    if settings.debug:
        print('[validate_measurement] rateTotal = %s' % rateTotal)

    # count request in last timespan
    rateConsumed = await countHitsForCaller(callerID, cassandra)
    if settings.debug:
        print('[validate_measurement] rateConsumed = %s' % rateConsumed)

    if rateTotal <= rateConsumed:
        raise HTTPException(429)
    else:
        # schedule marking this request for this client
        await logRequest(callerID, v_request.text, cassandra)

        # return
        return dress(validate(v_request.text))


@measurementRouter.get('/units')
async def get_all_units():
    """
        Get a list of all known unit symbols.
    """
    return sorted(getAllUnitSymbols())
