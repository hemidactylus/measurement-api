"""
    measurement.py
"""


from fastapi import APIRouter
# from typing import Optional
from pydantic import BaseModel

from dimLib.analyzer import validate, getAllUnitSymbols
from dimLib.formatting import dress


class ValidationRequest(BaseModel):
    text: str


measurementRouter = APIRouter()


@measurementRouter.post('/validate')
async def validate_measurement(v_request: ValidationRequest):
    """
    Validate a measurement.
    """
    return dress(validate(v_request.text))


@measurementRouter.get('/units')
async def get_all_units():
    """
        Get a list of all known unit symbols.
    """
    return sorted(getAllUnitSymbols())
