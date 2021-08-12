"""
    main.py
"""

from fastapi import FastAPI

from helpers.cors import addCors

from routers.measurement import measurementRouter


app = FastAPI()

addCors(app)

app.include_router(
    measurementRouter,
    prefix='/v1/measurement',
)
