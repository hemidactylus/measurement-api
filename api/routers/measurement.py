"""
    measurement.py
"""


from fastapi import APIRouter
from pydantic import BaseModel

from dimLib.analyzer import validate
from dimLib.formatting import dress


class RawMeasurement(BaseModel):
    text: str


measurementRouter = APIRouter()


@measurementRouter.post('/validate')
async def validate_measurement(raw_measurement: RawMeasurement):
    """
    Validate a measurement.
    """
    return dress(validate(raw_measurement.text))
