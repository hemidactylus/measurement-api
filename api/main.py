"""
    main.py
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .helpers.cors import addCors

from .routers.measurement import measurementRouter
from .routers.info import infoRouter

from dimLib.exceptions import MeasurementParseError

app = FastAPI()

addCors(app)


@app.exception_handler(MeasurementParseError)
async def parsing_exception_handler(request: Request,
                                    exc: MeasurementParseError):
    return JSONResponse(
        status_code=422,
        content={"message": exc.name},
    )

app.include_router(
    measurementRouter,
    prefix='/v1/measurement',
)

app.include_router(
    infoRouter,
    prefix='/v1/info',
)
