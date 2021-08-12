"""
    measurement.py
"""


from fastapi import APIRouter

measurementRouter = APIRouter()


@measurementRouter.get('/validate')
async def validateMeasurement():
    return {
        'dummy': 123,
    }
