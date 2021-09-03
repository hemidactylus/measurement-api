#!/bin/bash

DEBUG=true RATELIMITWINDOWSECONDS=20 ANONYMOUSRATEALLOWED=10 uvicorn api.main:app --reload
